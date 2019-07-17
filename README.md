# Robot Expressive Behavior Language (REBeL) - ReBeX (Robot Behavior Expression) - Behavior Expressions for Robots (BEER)

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

The meaning of the outcomes (in order):
-  turn left once and stop
-  turn left, turn right, and stop
-  turn left, turn right, go forward, and stop

## Union
Operator: `'+'`

Syntax: `'(+ [list of behaviors] [list of probabilities])'`

Example: `'(+ left right forward)'`

Possible outcomes:
- `left --> end`
- `right --> end`
- `forward --> end`

Union operation always __only return one of the arguments__.

By default, the union operation works probabilistically, and the probability for each argument is spread uniformly. For example, in the above expression has three operands, so the default probability for each operand is 1/3.

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

To force a deterministic number of loop/repetition, e.g. "loop *at least* `X` number of times", specify the probability > 1. For example, to repeat the `left` behavior __at least 2 times__:

`'(* left 2.3)'`

## The Vocabulary
The Vocabulary is the set of actions for the robot.

An entry in the Vocabulary is a pair of *name* and *value* for the action. The Name is represented by a string, no whitespace, short description for the action.

The Value can be *direct commands* or another expression. Examples of direct control:
- Joint angles for four DOFs/joints: `[0.3, 0.5, 0.5, 1.0]`
- Commands:
  - Turn LED on: `{'led': true}`
  - Speak: `{'say': 'hello world!'}`

### To add new actions to the vocabulary
Use the `.add(<name>, <value>)` method on the `vocab` object. `Name` is of type `string`, `Value` is restricted; a value of type `string` is considered an expression so it will be recursively evaluated, and non-`string` values such as `dictionary`, `float`, `list`, etc. will be the end values (will not be re-evaluated).

Examples
```python
from mjp import vocab

vocab.add('foo', [0.3, 0.5, 0.5, 1.0])  # Joint position for 4 DOF with name 'foo'
vocab.add('say_hello', {'say': 'hello world!'})  # Command to say 'hello world!' with name 'say_hello'
vocab.add('led_on', {'led': true})  # Command to turn on a LED with name 'led_on'

vocab.add('foo_hello_led', '(& foo say_hello led_on)')
```


**IMPORTANT**: The format of the commands depends on the format of the interfaces to your robot. So if you want to use/extend REBeL, you have to implement the interface between the result of REBeL parsing and to your robot yourself.


## Recursive Evaluation
REBeL evaluates each operand recursively until the operand cannot be expanded anymore. An expression can be given as an argument to any operation.

Example: `'(+ (& left right) right forward)'`

Possible outcomes:
- `(& left right) --> end` ==> `left --> right --> end`
- `right --> end`
- `forward --> end `

An expression can also be saved into another entry in the vocabulary and given a name, and can be called by the name it is assigned to.

Example:
```python
import rebel_parser as rp
import vocab

vocab.add('left_right', '(& left right)')  # First, add to vocabulary
combined = '(+ left_right right forward)'  # Use it in another expression

rp.parse(combined)  # Parsing this expression will give the same result as before

```

Currently, there is no specialized safety measure implemented to cause infinite recursion -- it will be caught by Python's interpreter.


## WORK IN PROGRESS
*Merging Logic*: an operation to mix two or more behaviors together into one behavior. For example: combining a behavior of looking left, and looking up, will result in the robot looking to upper left direction. Naturally, there are some behaviors that will not be able to be 'merged' such as: turning left with turning right, but turning left and going forward is still possible.

The logic is still under research.