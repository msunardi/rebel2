# Robot Expressive Behavior Logic (REBeL)

A framework to compose robot behaviors using algebraic expressions.

The first component of REBeL is the *operators*. There are three basic operations:
- **Concatenation**: putting two or more behaviors in a sequence
- **Union**: a set of actions to choose from
- **Loop**: repeating behavior

The second component is the *vocabulary*. The Vocabulary is the set of actions the robot can do. Each action has a *name* and *value*. The Name is the identifier for the action, e.g. `wave`, `turn_left`, `turn_right`, etc. The Value of an action has two types: *direct commands* and *expression*. 

As a Direct Command, it is the explicit values or commands that can be directly executed to control the robot, e.g. joint angles, turn LED on/off, etc. or some form of direct interface to the robot. As an Expression, the value is another REBeL expression, therefore it will be recursively expanded, until it can no longer be expanded, e.g. into a direct command. This is discussed more with examples in the Recursive Evaluation section below.

Each operation can be used deterministically or probabilistically.

Below are some examples of the usage.

Suppose the robot can do three actions: turning left, turning right, and go forward. To simplify, let's refer these as: `left`, `right`, and `forward`. Additionally, let's use `end` as the end of the behavior which means no action.

## Concatenation
Operator: `'&'`

Syntax: `'(& [list of behaviors] [list of proabilities])'`

Example: `'(& left right forward)'`

Outcome: `left --> right --> forward --> end.`

By default, the concatenation operation works deteriminstically.

When used probabilistically, the semantic is: "the probability of continuing the sequence vs. ending the sequence". To use concatenation probabilistically, add probability arguments.

Example: `'(& left right forward 0.5)'`

Possible outcomes:
- `left --> end`
- `left --> right --> end`
- `left --> right --> forward --> end`


## Union
Operator: `'+'`

Syntax: `'(+ [list of behaviors] [list of probabilities])'`

Example: `'(+ left right forward)'`

Possible outcomes:
- `left --> end`
- `right --> end`
- `forward --> end`

Union operation always only return one of the arguments. By default, the union operation works probabilistically, and the probability for each argument is spread uniformly.

For example, the probability for each argument in the above expression is 1/3.

To specify individual probabilities for each argument, provide a list of probabilities. For example, to give `left` probability `0.2`, `right` to `0.3`, and `forward` to `0.5`.

`'(+ left right forward [0.2, 0,3, 0.5])'`


## Loop/Repetition
Operator: `'*'`

Syntax: `'(* behavior probability[=0.5])'`

Future expansion: `'(* behavior [list of probability])'`

Example: `'(* left)'`

Semantic: repeat the behavior 0 or more times. By default, if not provided explicitly, the probability is `0.5`.

Possible outcomes:
- `end` (nothing done)
- `left --> end`
- `left --> left --> end`
- `left --> ... --> left --> end`

To force a deterministic number of loop/repetition, e.g. "loop *at least* x number of times", specify the probability > 1. For example, to repeat the `left` behavior *at least 2 times*:

`'(* left 2.3)'`

## The Vocabulary
The Vocabulary is the set of actions for the robot.

An entry in the Vocabulary is a pair of *name* and *value* for the action. The Name is represented by a string, no whitespace, short description for the action.

The Value can be *direct commands* or another expression. Examples of direct control:
- Joint angles for four DOFs/joints: `[0.3, 0.5, 0.5, 1.0]`
- Commands:
  - Turn LED on: `{'led': true}`
  - Speak: `{'say': 'hello world!'}`

**IMPORTANT**: The format of the commands depends on the format of the interfaces to your robot. So if you want to use/extend REBeL, you need to implement the interface between the result of REBeL parsing and to your robot.



## Recursive Evaluation
REBeL evaluates each operand recursively until the operand cannot be expanded anymore. An expression can be given as an argument to any operation.

Example: `'(+ (& left right) right forward)'`

Possible outcomes:
- `(& left right) --> end` ==> `left --> right --> end`
- `right --> end`
- `forward --> end `

An expression can also be saved into another entry in the vocabulary and given a name, and can be called by the name it is assigned to.

Currently, there is no specialized safety measure implemented to cause infinite recursion -- it will be caught by Python's interpreter.


## WORK IN PROGRESS
*Merging Logic*: an operation to mix two or more behaviors together into one behavior. For example: combining a behavior of looking left, and looking up, will result in the robot looking to upper left direction. Naturally, there are some behaviors that will not be able to be 'merged' such as: turning left with turning right, but turning left and going forward is still possible.

The logic is still under research.