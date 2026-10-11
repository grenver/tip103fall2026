# Guide for Writing Problem Set Explanations

Use this guide when creating or revising a problem set Markdown file. The goal is to help students understand a concept, use it to solve a problem through **UPI: Understand, Plan, Implement**, and explain their decisions in an interview.

A finished explanation should let a student answer: What did I learn? What clues tell me to use it? How does it make the solution work? Can I apply it to a different problem?

## Teaching approach

1. Identify the central concept before writing the solution. Choose a specific idea such as “advance a reference to visit the next node,” rather than a broad topic such as “linked lists.” Some problems combine concepts; name the main one and the supporting prerequisites.
2. Explain the prerequisite in plain language with a small example. Do not assume students already understand syntax such as `self`, `is`, `popleft()`, or `.next`.
3. Connect a clue in the problem to that concept. Explain the reasoning that selects the approach; simply naming a pattern is insufficient.
4. Build the plan before showing code. State what information is tracked, how it changes, and when processing stops.
5. Trace a small example, including the step where the key decision happens. Then translate the plan into readable code.
6. Check understanding with a prediction or a small variation. Students should explain why their answer works, not just reproduce it.

Introduce concepts in steps across the set. Briefly reuse established ideas and teach each new idea where it first becomes necessary. Do not force every exercise into a sophisticated algorithm pattern: object construction and reference assignment are learning goals too.

## Begin each problem set with a concept map

Use a short table to show the progression:

| Problem | Main concept | Prerequisite | What the student should be able to explain |
| --- | --- | --- | --- |
| Villager Class | Instance state | Functions and lists | Why each villager needs its own furniture list |
| Add Furniture | Validate before changing state | Attributes and membership | Why an invalid item must not reach `append()` |
| Group by Personality | Filter objects and collect an attribute | Loops and attributes | Why the result contains names rather than objects |
| Telephone | Traverse object references | Identity and references | How moving to a neighbor progresses toward the target |
| Linked Up | Connect nodes through references | Objects and `None` | Why assigning `.next` creates a link without copying a node |

These are examples from Week 4 Session 1. Write a new map for each set using its actual requirements.

## Clear labels and concise navigation

Apply these conventions to both Markdown and Python files:

- Label every exercise **Problem N: Exact supplied title**. Add the function or class name and a short method label when useful, especially for similarly named exercises (for example, BFS versus DFS).
- Start Markdown with a compact problem index/concept map containing the problem number, exact title, callable, and main concept. Link each row to its problem heading.
- Use the same numbered title in a visible Python comment banner immediately before each solution. Separate **U — Understand**, **P — Plan**, and **I — Implement**; do not bury the title in a numbered U comment.
- Clearly label shared imports/helpers and example checks so they cannot be mistaken for another problem. Label checks by problem number and title.
- If two prompts use the same function name, preserve both implementations with an explicitly documented alias, or separate files. State how to use the required name for an individual submission.
- Keep UPI as the core. Prefer a few concrete sentences, a short plan, and one useful trace over repeated explanations. Combine learning goal, concept, and recognition clue when they overlap. Keep mistakes, interview guidance, and questions brief; avoid repeating the same point across sections.
- Put assumptions and prompt errors beside the affected problem. Never silently change an example or teach an incorrect hint.

## Template for each problem

Copy and fill in the following structure. Keep simple problems short; expand the sections where students need more support.

## Problem [Number]: [Exact problem title] — `[function or class]`

**Learning goal:** After this problem, you should be able to [specific, observable skill].

**Key concept:** [Name the central idea and explain how it works in plain language. Include a tiny example if needed.]

**What points us toward this concept?** [Quote or paraphrase a requirement, then explain why it suggests this approach.]

#### U — Understand

- **Input:** [Type and meaning; include the supplied objects or starting state.]
- **Output or effect:** [Exact return type, or the required change to an object. Distinguish returning from printing.]
- **Rules:** [Ordering, allowed operations, duplicates, mutation, and other relevant constraints.]
- **Example:** [Small input and expected result, with an explanation.]
- **Questions or assumptions:** [Only meaningful ambiguities. Clearly mark assumptions rather than inventing requirements.]

#### P — Plan

Explain the steps in plain language before code:

1. [Set up the state and explain what each variable represents.]
2. [Describe the decision and update performed at each step.]
3. [Explain when to stop and what to return or change.]

**Why the plan works:** [State what stays true as the algorithm proceeds and why the final state meets the requirement. Use an intuitive explanation before introducing the term “invariant.” For a loop, explain why it makes progress and terminates.]

**Trace:** [Show a few steps of one small example. Track the variables that matter. Include an informative boundary or decision, not just a list of final outputs.]

#### I — Implement

```python
# Translate the plan into clear code here.
# Comments should explain decisions, not repeat the syntax.
```

**Connect the code to the plan:** [Explain the unfamiliar or decisive lines. State what the operation returns and whether it changes a collection or reference.]

**Check the solution:** [Walk through the normal example and the relevant boundary cases. Explain what each case verifies. Do not prescribe cases outside the input contract.]

**Cost:** [Define n. Explain which operations account for time and memory. Distinguish auxiliary space from returned output when helpful.]

#### Common mistakes

Explain two or three likely mistakes as **mistake → consequence → correction**. Choose mistakes specific to this concept and show a tiny counterexample when useful.

#### Interview explanation

Give a short model explanation that includes the requirement, selected approach, why it works, and its cost. Treat it as an example of reasoning, not a script to memorize. Include a clarifying question only if the prompt leaves something relevant unspecified.

#### Check your understanding

Ask one prediction question and one small transfer question. Put answers in a collapsible section so students can try first:

<details>
<summary>Reasoning and answers</summary>

[Explain the reasoning, not only the answer.]

</details>

## Offer support before the full solution

For practice materials, put the implementation in a collapsible section or below a clearly marked solution boundary. Provide hints that reveal the reasoning in stages:

1. A question directing attention to the relevant requirement.
2. A clue about what information to track.
3. A more concrete next step or pseudocode.

Do not reveal the full implementation in the first hint. For review materials, visible solutions are fine, but keep Understand and Plan before Implement.

## Examples of teaching the missing piece

### Queue processing

The missing piece may be that **removing an item from a queue does not mean approving it**. `popleft()` removes and returns one front item. A regular queue preserves arrival order; it does not automatically prioritize smaller values.

For the blueprint problem, connect that fact to the rule: if a simpler blueprint is still waiting, the removed blueprint must wait again. A queue simulation can move it to the back; otherwise it can be added to the approved result. Trace `[3, 1, 2]` to show why `3` waits and `1` is approved first.

If comparing alternatives, explain their behavior: a priority queue selects the minimum directly, while insertion into a sorted result rearranges the result as items arrive. Producing a sorted result alone does not explain the simulated waiting process. Respect an explicit queue requirement and teach the chosen mechanism accurately.

### Reference traversal

The missing piece may be that **a variable can refer to a different object without changing the links**. In `current = current.neighbor`, the traversal variable moves to the next object; it does not move or copy the villager.

Trace `A -> B -> C -> None`: test A, advance to B, test B, advance to C. Explain why comparing to a target instance uses identity (`is`) when the task asks for that exact object. Matching names would not establish that it is the same instance.

Address cycles according to the prompt. If cycles are allowed, explain why a visited set prevents repeated traversal and adds memory cost. If the prompt guarantees an acyclic chain, teach the simpler traversal first and label cycle handling as an extension.

## Avoid these explanation habits

- Jumping from the story directly to finished code.
- Saying “use a queue” or “use two pointers” without explaining why.
- Introducing several new concepts at once without prerequisites.
- Treating an output example as proof that the algorithm always works.
- Encouraging students to memorize code or identify patterns only from story keywords.
- Claiming a collection has behavior it does not have, such as automatic sorting in `deque`.
- Adding defensive behavior or advanced abstractions without explaining whether the prompt requires them.
- Hiding implementation costs such as repeated `min()`, list insertion, slicing, or searches.
- Letting file organization introduce extra learning requirements. If exercises change a constructor, explain each version; inheritance used to combine solutions is a packaging choice unless the exercise teaches inheritance.
- Inventing missing problem statements or changing the required interface.

## Review before saving

- Are every problem title, UPI section, and example-check block clearly labeled in both files?
- Does the file preserve the prompt's interface, rules, and examples?
- Is the central concept explicit and connected to a requirement?
- Are prerequisites explained before they are used?
- Does the plan exist independently of the code?
- Does the trace expose the key decision and show progress?
- Are code, explanation, and complexity consistent?
- Can students explain why the result is correct and when the algorithm stops?
- Do checks cover meaningful cases such as empty input, duplicates, or reference identity when applicable?
- Is there an opportunity to reason before reading the solution?
- Does the interview explanation model reasoning rather than memorization?
- Are missing requirements and optional extensions clearly labeled?

## Reusable request for future files

> Create or revise the problem set Markdown using `PROBLEM_SET_WRITING_GUIDE.md`. Preserve the supplied requirements and interfaces. Start with a concept progression map. For each problem, teach the key concept and its recognition clue, then use Understand, Plan, Implement with a small trace, a correctness explanation, meaningful checks, and justified complexity. Include common mistakes, a brief interview explanation, and prediction and transfer questions with hidden answers. Keep the depth appropriate to the exercise, and mark any missing requirements instead of inventing them.
