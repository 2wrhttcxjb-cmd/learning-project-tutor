#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"

def load_yaml(path)
  return {} unless File.exist?(path)

  YAML.load_file(path) || {}
end

def section_body(text, heading)
  match = text.match(/^#{Regexp.escape(heading)}\s*$\n(.*?)(?=^##\s|\z)/m)
  match ? match[1].strip : ""
end

def file_nonempty?(path)
  File.exist?(path) && !File.read(path, encoding: "UTF-8").strip.empty?
end

def run_step(cmd)
  success = system(cmd)
  raise "Command failed: #{cmd}" unless success
end

topic = ARGV[0]
abort("Usage: ruby tools/run_learning_cycle.rb <topic>") if topic.to_s.empty?

repo_root = File.expand_path("..", __dir__)
topic_dir = File.join(repo_root, "topics", topic)
state_path = File.join(topic_dir, "topic_state.yaml")
abort("Topic state not found: #{state_path}") unless File.exist?(state_path)

state = load_yaml(state_path)
status = state["status"].to_s
summary = {
  "topic" => topic,
  "status" => status,
  "next_action" => nil,
  "memory_writeback" => "not_applicable",
  "preflight" => [],
  "blockers" => []
}

case status
when "drafting_map"
  source_path = File.join(topic_dir, "00-source.md")
  if file_nonempty?(source_path)
    summary["next_action"] = "generate_course_map"
  else
    summary["blockers"] << "missing or empty 00-source.md"
  end
when "ready_for_lesson"
  summary["next_action"] = "generate_lesson"
when "waiting_user_response"
  response_ref = state["current_response_file"].to_s
  response_path = File.join(topic_dir, response_ref)
  if file_nonempty?(response_path)
    run_step("python3 tools/validate_lesson_qa.py #{topic}")
    summary["preflight"] << "qa_validated"
    run_step("python3 tools/build_quote_index.py #{topic}")
    summary["preflight"] << "quote_index_refreshed"
    summary["next_action"] = "generate_diagnosis"
  else
    summary["blockers"] << "response file missing or empty: #{response_ref}"
  end
when "ready_for_diagnosis"
  lesson_ref = state["current_lesson_file"].to_s
  response_ref = state["current_response_file"].to_s
  summary["blockers"] << "missing lesson file: #{lesson_ref}" unless file_nonempty?(File.join(topic_dir, lesson_ref))
  summary["blockers"] << "missing response file: #{response_ref}" unless file_nonempty?(File.join(topic_dir, response_ref))
  if summary["blockers"].empty?
    run_step("python3 tools/validate_lesson_qa.py #{topic}")
    summary["preflight"] << "qa_validated"
    summary["next_action"] = "generate_diagnosis"
  end
when "ready_for_next_action"
  run_step("ruby tools/write_memory_update.rb #{topic} lesson")
  summary["memory_writeback"] = "lesson"
  decision = state["last_decision"].to_s
  summary["next_action"] =
    case decision
    when "advance" then "generate_next_lesson_or_final_transition"
    when "bridge" then "generate_bridge_lesson"
    when "reframe" then "generate_reframe_lesson"
    else "inspect_latest_diagnosis"
    end
when "final_synthesis_ready"
  summary["next_action"] = "generate_final_synthesis"
when "final_transfer_ready"
  summary["next_action"] = "generate_final_transfer"
when "waiting_transfer_response"
  transfer_path = File.join(topic_dir, "final", "02-transfer.md")
  if File.exist?(transfer_path) && !section_body(File.read(transfer_path, encoding: "UTF-8"), "## User Response").empty?
    summary["next_action"] = "generate_transfer_diagnosis"
  else
    summary["blockers"] << "final/02-transfer.md User Response is empty"
  end
when "ready_for_transfer_diagnosis"
  summary["next_action"] = "generate_transfer_diagnosis"
when "final_articulation_ready"
  summary["next_action"] = "generate_final_articulation"
when "waiting_articulation_response"
  articulation_path = File.join(topic_dir, "final", "03-articulation.md")
  if File.exist?(articulation_path) && !section_body(File.read(articulation_path, encoding: "UTF-8"), "## User Response").empty?
    summary["next_action"] = "advance_to_closure"
  else
    summary["blockers"] << "final/03-articulation.md User Response is empty"
  end
when "ready_for_closure"
  run_step("ruby tools/write_memory_update.rb #{topic} topic")
  summary["memory_writeback"] = "topic"
  summary["next_action"] = "generate_final_closure"
when "closed"
  summary["next_action"] = "none"
else
  summary["blockers"] << "unknown status: #{status}"
end

puts YAML.dump(summary)
