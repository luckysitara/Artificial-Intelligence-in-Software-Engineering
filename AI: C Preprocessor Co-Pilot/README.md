# AI: C Preprocessor Co-Pilot

### Task Description
This task demonstrates the use of AI as a Macro Safety Inspector and Conditional Code Generator. The goal was to identify common C Preprocessor pitfalls, such as operator precedence errors, and generate robust, conditionally compiled scaffolding.

### AI Tool Used
* **Gemini 3 Flash**

### Files & Resources
* [multiply_unsafe.c](./multiply_unsafe.c): The initial, flawed macro susceptible to precedence bugs.
* [math_utils_safe.h](./math_utils_safe.h): The refactored, robust header file with include guards and conditional logic.
* [Screenshots/](./Screenshots/): Documentation of the prompts used to guide the AI.

### Analysis & Reflection
Using AI to audit C macros is highly effective because macros are literal text substitutions that don't follow standard C scope or precedence rules. The AI successfully identified that `MULTIPLY(2+3, 4)` would expand incorrectly and suggested a parenthesized version to ensure logical integrity.
