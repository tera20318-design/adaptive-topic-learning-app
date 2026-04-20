# Research Brief

- Run ID: 20260419-094726-research
- Topic: スモークテスト用の産業調査
- Output language: Japanese
- Research mode: gpt-like
- Research preset: dr_output
- As-of date: 2026-04-19
- Candidate collection target: 1280
- Deep-read target: 104
- Topic breadth class: standard (標準)
- Topic breadth score: 55
- Topic budget scale: 1.00
- Topic stop profile: standard / 標準 / score 55; floors q=40, candidates=359, deep=37; stop novelty=0.0350, same-domain=0.1600
- Entity discovery mode: auto
- Discovery kind: company (`inferred`, score 32)
- Discovery bundle: 企業・事業所ロスター
- Entity discovery profile: auto / optional / kind company / bundle 企業・事業所ロスター; score 32; surface_floor=0, tail_queries=0
- Generated at: 2026-04-19 09:47:26

## Core question

-

## User constraints

-

## Must-cover angles

-

## Reader decisions to support

-

## Must-not-miss risks

-

## Assumptions

-

## Preferred domains

-

## Excluded angles

-

## Checklist ideas

-

## Tail sweep

- If discovery is required, use the bundle that matches the topic kind: company, event, technology, policy, product, or general.
- Keep `notes/entity-roster.md` updated with must-find surfaces, confirmed surfaces, and missing surfaces.

## Stop rule

Stop after the deep-read target is met and newly surfaced sources add little novelty. Use the topic stop profile to decide how long to keep exploring: broad topics may continue longer while source classes are still changing, while narrow topics may stop earlier once the coverage map stabilizes.
