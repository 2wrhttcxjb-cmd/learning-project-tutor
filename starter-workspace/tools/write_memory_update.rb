#!/usr/bin/env ruby
# frozen_string_literal: true

require "date"
require "yaml"

def read_text(path)
  File.read(path, encoding: "UTF-8")
end

def write_text(path, text)
  File.write(path, text, encoding: "UTF-8")
end

def load_yaml(path)
  return {} unless File.exist?(path)

  YAML.load_file(path) || {}
end

def write_yaml(path, data)
  File.write(path, YAML.dump(data), encoding: "UTF-8")
end

def topic_slug(topic)
  topic.downcase.gsub(/[^a-z0-9]+/, "-").gsub(/^-|-$/, "")
end

def extract_section(text, heading)
  pattern = /^#{Regexp.escape(heading)}\s*$\n(.*?)(?=^##\s|\z)/m
  match = text.match(pattern)
  match ? match[1].strip : nil
end

def compact_line(text)
  text.to_s.lines.map(&:strip).reject(&:empty?).join(" ").gsub(/\s+/, " ").strip
end

def bullet_list(items, indent = "  - ")
  items.map { |item| "#{indent}`#{item}`" }.join("\n")
end

def ensure_markdown_heading(text, heading)
  return text if text.include?(heading)

  text = text.rstrip + "\n\n" unless text.empty?
  text + "#{heading}\n"
end

def append_markdown_entry(path, heading, entry)
  text = File.exist?(path) ? read_text(path) : ""
  text = ensure_markdown_heading(text, heading)
  text = text.rstrip + "\n\n" + entry.rstrip + "\n"
  write_text(path, text)
end

def uniq_merge(values, additions)
  ((values || []) + (additions || [])).compact.uniq
end

def ensure_node(nodes, attrs)
  node = nodes.find { |item| item["id"] == attrs["id"] }
  if node
    node["source_refs"] = uniq_merge(node["source_refs"], attrs["source_refs"])
    node["topic_refs"] = uniq_merge(node["topic_refs"], attrs["topic_refs"])
    node["summary"] = attrs["summary"] if node["summary"].to_s.strip.empty? && attrs["summary"]
    node["activation_score"] = [node["activation_score"].to_f, attrs["activation_score"].to_f].max.round(2)
  else
    nodes << attrs
  end
end

def ensure_edge(edges, attrs)
  edge = edges.find do |item|
    item["from"] == attrs["from"] && item["to"] == attrs["to"] && item["type"] == attrs["type"]
  end
  if edge
    edge["weight"] = [edge["weight"].to_f, attrs["weight"].to_f].max.round(2)
    edge["evidence_refs"] = uniq_merge(edge["evidence_refs"], attrs["evidence_refs"])
    edge["last_updated_at"] = attrs["last_updated_at"]
  else
    edges << attrs
  end
end

def touch_existing_nodes(nodes, node_ids, source_refs, increment)
  nodes.each do |node|
    next unless node_ids.include?(node["id"])

    node["source_refs"] = uniq_merge(node["source_refs"], source_refs)
    node["activation_score"] = [[node["activation_score"].to_f + increment, 1.0].min.round(2), 0.1].max
  end
end

def touch_existing_edges(edges, node_ids, source_refs, date, increment)
  edges.each do |edge|
    next unless node_ids.include?(edge["from"]) && node_ids.include?(edge["to"])

    edge["evidence_refs"] = uniq_merge(edge["evidence_refs"], source_refs)
    edge["weight"] = [[edge["weight"].to_f + increment, 1.0].min.round(2), 0.1].max
    edge["last_updated_at"] = date
  end
end

def update_schema_index(path, topic)
  return unless File.exist?(path)

  text = read_text(path)
  return if text.include?("- `#{topic}`")

  text = text.sub(/(^- connected topics:\n(?:  - .+\n)*)/m) do |block|
    block.rstrip + "\n  - `#{topic}`\n"
  end
  write_text(path, text)
end

def default_activated_nodes(topic_memory)
  refs = topic_memory.fetch("node_refs", {})
  ids = []
  ids.concat(refs.fetch("concepts", []))
  ids.concat(refs.fetch("schemas", []))
  ids.concat(refs.fetch("episodes", []))
  ids.first(3).map { |id| { "id" => id } }
end

def activated_node_ids(topic_state, topic_memory)
  nodes = topic_state["last_activated_nodes"]
  nodes = default_activated_nodes(topic_memory) if nodes.nil? || nodes.empty?
  nodes.map do |entry|
    if entry.is_a?(Hash)
      entry["id"] || "#{entry.keys.first}:#{entry.values.first}"
    else
      entry.to_s
    end
  end.compact
end

def build_lesson_context(diagnosis_ref, recon_text, activated_nodes)
  <<~MD
# Current Memory Context

## Activation Source
- current trigger: `#{diagnosis_ref}`
- activation kind: lesson-level reconsolidation
- activated nodes:
#{bullet_list(activated_nodes)}

## Why It Was Activated
#{recon_text}

## Teaching Use
- read this before generating the next lesson / bridge / reframe / final transition
- keep cross-topic recall lightweight and subordinate to the current topic's main line

## Guardrails
- do not let old topics replace current-topic evidence
- keep QA as auxiliary evidence only
  MD
end

def build_closed_context(topic, status, activated_nodes)
  <<~MD
# Current Memory Context

## Status
- topic: `#{topic}`
- state: `#{status}`
- note: this topic is closed, so there is no active teaching workset

## Last Closure Writeback
- activated nodes:
#{bullet_list(activated_nodes)}
- use this topic as a retrievable closed-memory source for future cross-topic activation
  MD
end

topic = ARGV[0]
mode = ARGV[1]
if topic.to_s.empty? || !%w[lesson topic].include?(mode)
  warn "Usage: ruby tools/write_memory_update.rb <topic> <lesson|topic>"
  exit 1
end

repo_root = File.expand_path("..", __dir__)
topic_dir = File.join(repo_root, "topics", topic)
state_path = File.join(topic_dir, "topic_state.yaml")
abort("Topic state not found: #{state_path}") unless File.exist?(state_path)

today = Date.today.iso8601
topic_state = load_yaml(state_path)
topic_memory_path = File.join(topic_dir, "memory", "topic-memory.yaml")
topic_memory = load_yaml(topic_memory_path)
activated_nodes = activated_node_ids(topic_state, topic_memory)

if mode == "lesson"
  current_key = topic_state["current_diagnosis_file"].to_s
  last_key = topic_state["last_lesson_memory_writeback_key"].to_s
  if !current_key.empty? && current_key == last_key
    puts "Memory writeback skipped for #{topic} (lesson): already applied to #{current_key}"
    exit 0
  end
elsif mode == "topic"
  current_key = "topic-closure"
  last_key = topic_state["last_topic_memory_writeback_key"].to_s
  if current_key == last_key
    puts "Memory writeback skipped for #{topic} (topic): already applied"
    exit 0
  end
end

memory_state_path = File.join(repo_root, "memory", "memory_state.yaml")
nodes_path = File.join(repo_root, "memory", "nodes.yaml")
edges_path = File.join(repo_root, "memory", "edges.yaml")
schema_index_path = File.join(repo_root, "memory", "schema-index.md")
activation_log_path = File.join(repo_root, "memory", "activation-log.md")
history_path = File.join(topic_dir, "memory", "reconsolidation-history.md")
current_context_path = File.join(topic_dir, "memory", "current-context.md")

memory_state = load_yaml(memory_state_path)
nodes_data = load_yaml(nodes_path)
edges_data = load_yaml(edges_path)
nodes = nodes_data["nodes"] ||= []
edges = edges_data["edges"] ||= []

source_refs = []
summary = nil

if mode == "lesson"
  diagnosis_ref = topic_state["current_diagnosis_file"]
  lesson_ref = topic_state["current_lesson_file"]
  response_ref = topic_state["current_response_file"]
  abort("current_diagnosis_file missing") unless diagnosis_ref

  diagnosis_path = File.join(topic_dir, diagnosis_ref)
  diagnosis_text = read_text(diagnosis_path)
  recon_text = extract_section(diagnosis_text, "## 9. Reconsolidation update") || "No explicit reconsolidation note recorded."
  summary = compact_line(recon_text)
  source_refs = [lesson_ref, response_ref, diagnosis_ref].compact.map { |ref| File.join("topics", topic, ref) }

  write_text(current_context_path, build_lesson_context(diagnosis_ref, recon_text, activated_nodes))

  append_markdown_entry(
    history_path,
    "# Reconsolidation History",
    <<~MD
      ## #{today}
      - trigger: `#{diagnosis_ref}` completed; system prepared the next teaching action
      - qa scope: `Lesson #{File.basename(lesson_ref.to_s, ".md")}`
      - activated nodes:
#{bullet_list(activated_nodes)}
      - strengthened understanding:
        - #{summary}
      - writeback result:
        - updated `memory/current-context.md`
        - appended lesson-level reconsolidation to global activation log
    MD
  )

  append_markdown_entry(
    activation_log_path,
    "# Activation Log",
    <<~MD
      ### #{today}
      - current topic / lesson: `#{topic}` / `#{File.basename(lesson_ref.to_s, ".md")}`
      - activation kind: lesson-level
      - activated nodes:
#{bullet_list(activated_nodes)}
      - trigger reason:
        - #{summary}
      - edge updates:
        - strengthened existing topic-linked memory edges with the latest lesson evidence
      - QA/response inconsistency if any:
        - none newly detected during writeback
      - teaching implication:
        - next action should read `topics/#{topic}/memory/current-context.md` before generating new teaching content
    MD
  )

  touch_existing_nodes(nodes, activated_nodes, source_refs, 0.04)
  touch_existing_edges(edges, activated_nodes, source_refs, today, 0.03)
elsif mode == "topic"
  final_dir = File.join(topic_dir, "final")
  synthesis_ref = File.join("final", "01-synthesis.md")
  transfer_ref = File.join("final", "02-transfer.md")
  articulation_ref = File.join("final", "03-articulation.md")
  closure_ref = File.join("final", "README.md")
  synthesis_path = File.join(topic_dir, synthesis_ref)
  abort("Final synthesis not found: #{synthesis_path}") unless File.exist?(synthesis_path)

  synthesis_text = read_text(synthesis_path)
  core_claim = extract_section(synthesis_text, "## 1. Core claim") || "Topic closure strengthened this topic's stable schema."
  summary = compact_line(core_claim)
  source_refs = [synthesis_ref, transfer_ref, articulation_ref, closure_ref]
                .map { |ref| File.join("topics", topic, ref) }
                .select { |ref| File.exist?(File.join(repo_root, ref)) }

  primary_concept = topic_memory.dig("node_refs", "concepts")&.first
  primary_schema = topic_memory.dig("node_refs", "schemas")&.first
  closure_node_id = "episode:#{topic_slug(topic)}-topic-closure"

  ensure_node(
    nodes,
    {
      "id" => closure_node_id,
      "label" => "#{topic_state["topic_title"]} topic closure",
      "type" => "episode",
      "source_refs" => source_refs,
      "topic_refs" => [topic],
      "summary" => summary,
      "activation_score" => 0.72
    }
  )

  ensure_edge(
    edges,
    {
      "from" => closure_node_id,
      "to" => primary_concept,
      "type" => "indexes",
      "weight" => 0.82,
      "evidence_refs" => source_refs,
      "last_updated_at" => today
    }
  ) if primary_concept

  ensure_edge(
    edges,
    {
      "from" => closure_node_id,
      "to" => primary_schema,
      "type" => "supports",
      "weight" => 0.8,
      "evidence_refs" => source_refs,
      "last_updated_at" => today
    }
  ) if primary_schema

  closure_activated = (activated_nodes + [closure_node_id]).uniq
  topic_memory["node_refs"] ||= {}
  topic_memory["node_refs"]["episodes"] = uniq_merge(topic_memory.dig("node_refs", "episodes"), [closure_node_id])
  touch_existing_nodes(nodes, closure_activated, source_refs, 0.06)
  touch_existing_edges(edges, closure_activated, source_refs, today, 0.04)
  update_schema_index(schema_index_path, topic)
  write_text(current_context_path, build_closed_context(topic, topic_state["status"], closure_activated))

  append_markdown_entry(
    history_path,
    "# Reconsolidation History",
    <<~MD
      ## #{today}
      - trigger: topic closure completed
      - activation kind: topic-level
      - activated nodes:
#{bullet_list(closure_activated)}
      - strengthened understanding:
        - #{summary}
      - writeback result:
        - wrote closure-strengthened memory back to global nodes / edges
        - updated closed-topic `memory/current-context.md`
    MD
  )

  append_markdown_entry(
    activation_log_path,
    "# Activation Log",
    <<~MD
      ### #{today}
      - current topic / lesson: `#{topic}` / `topic closure`
      - activation kind: topic-level
      - activated nodes:
#{bullet_list(closure_activated)}
      - trigger reason:
        - final synthesis, transfer, articulation, and closure jointly stabilized this topic as a reusable memory source
      - edge updates:
        - added or strengthened closure-level links from the topic to its core concept and schema
      - QA/response inconsistency if any:
        - none
      - teaching implication:
        - future topics may retrieve this topic as a closed-memory source instead of an active teaching workset
    MD
  )

  activated_nodes = closure_activated
end

memory_state["graph_version"] = memory_state["graph_version"] || 1
memory_state["status"] = "active"
memory_state["last_reconsolidated_at"] = today
memory_state["last_active_topic"] = topic
memory_state["last_writeback_summary"] = summary

topic_memory["last_reconsolidated_at"] = today
topic_state["last_activation_at"] = today
topic_state["last_activated_nodes"] = activated_nodes.map do |id|
  parts = id.split(":", 2)
  { parts[0] => parts[1] || id }
end
topic_state["reconsolidation_needed"] = false
if mode == "lesson"
  topic_state["last_lesson_memory_writeback_key"] = topic_state["current_diagnosis_file"]
elsif mode == "topic"
  topic_state["last_topic_memory_writeback_key"] = "topic-closure"
end

write_yaml(memory_state_path, memory_state)
write_yaml(nodes_path, nodes_data)
write_yaml(edges_path, edges_data)
write_yaml(topic_memory_path, topic_memory)
write_yaml(state_path, topic_state)

puts "Memory writeback complete for #{topic} (#{mode})"
