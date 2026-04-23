# State Machine

这是对学习状态机的分发版摘要。

## Core statuses
- `drafting_map`: 根据 source 生成 `00-course-map.md`
- `ready_for_lesson`: 生成下一节 lesson
- `waiting_user_response`: 等待正式 response
- `ready_for_diagnosis`: 读取 lesson 和 response 生成 diagnosis
- `ready_for_next_action`: 根据 diagnosis 决定下一步

## Final statuses
- `final_synthesis_ready`
- `final_transfer_ready`
- `waiting_transfer_response`
- `ready_for_transfer_diagnosis`
- `final_articulation_ready`
- `waiting_articulation_response`
- `ready_for_closure`
- `closed`

## Transition rules
- 每次运行默认只做一个正式状态迁移
- `waiting_*_response` 状态下，如果 response 已完成，可以直接推进到下一步
- `ready_for_next_action` 会先做记忆回写，再决定是否 `advance` / `bridge` / `reframe`
- transfer 失败时，必须重开学习环路，不能直接关闭 topic

## Validation rules
- 缺 response 时不继续
- 状态与文件引用不一致时，先报告不一致
- QA 记录只能作为辅助证据读取

## Useful scripts
- `scripts/scaffold_learning_workspace.py`
- `scripts/create_topic_from_template.py`
- `scripts/run_learning_cycle.rb`
- `scripts/validate_lesson_qa.py`
- `scripts/build_quote_index.py`
