# 📐 Quadratic Equations Complete Guide

## What is a Quadratic Equation?

**Definition:** An equation where the highest power of the variable is 2

**Standard Form:**
$$\boxed{ax^2 + bx + c = 0}$$

Where:
- $a$ = coefficient of $x^2$ (must not be zero!)
- $b$ = coefficient of $x$
- $c$ = constant term
- $x$ = variable (unknown)

**Examples:**
- $x^2 + 5x + 6 = 0$ (a=1, b=5, c=6)
- $2x^2 - 3x + 1 = 0$ (a=2, b=-3, c=1)
- $x^2 - 4 = 0$ (a=1, b=0, c=-4)

---

# 🎯 Four Methods to Solve

## Method 1: Quadratic Formula (Works for All!)

**The Formula:**
$$\boxed{x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}}$$

**This ALWAYS works for any quadratic equation!**

---

### Step-by-Step Process

**Step 1:** Identify $a$, $b$, and $c$

**Step 2:** Substitute into formula

**Step 3:** Calculate discriminant: $\Delta = b^2 - 4ac$

**Step 4:** Simplify

---

### Example 1: $x^2 + 5x + 6 = 0$

**Step 1:** Identify coefficients
- $a = 1$
- $b = 5$
- $c = 6$

**Step 2:** Substitute into formula
$$x = \frac{-5 \pm \sqrt{5^2 - 4(1)(6)}}{2(1)}$$

**Step 3:** Calculate discriminant
$$\Delta = 5^2 - 4(1)(6) = 25 - 24 = 1$$

**Step 4:** Simplify
$$x = \frac{-5 \pm \sqrt{1}}{2}$$

$$x = \frac{-5 \pm 1}{2}$$

**Two solutions:**

$$x_1 = \frac{-5 + 1}{2} = \frac{-4}{2} = -2$$

$$x_2 = \frac{-5 - 1}{2} = \frac{-6}{2} = -3$$

**Answer:** $x = -2$ or $x = -3$

---

### Example 2: $2x^2 - 7x + 3 = 0$

**Step 1:** Identify
- $a = 2$
- $b = -7$
- $c = 3$

**Step 2:** Substitute
$$x = \frac{-(-7) \pm \sqrt{(-7)^2 - 4(2)(3)}}{2(2)}$$

**Step 3:** Calculate
$$x = \frac{7 \pm \sqrt{49 - 24}}{4}$$

$$x = \frac{7 \pm \sqrt{25}}{4}$$

$$x = \frac{7 \pm 5}{4}$$

**Two solutions:**

$$x_1 = \frac{7 + 5}{4} = \frac{12}{4} = 3$$

$$x_2 = \frac{7 - 5}{4} = \frac{2}{4} = \frac{1}{2}$$

**Answer:** $x = 3$ or $x = \frac{1}{2}$

---

### Example 3: $x^2 + 4x + 1 = 0$

**Step 1:** Identify
- $a = 1$
- $b = 4$
- $c = 1$

**Step 2:** Substitute
$$x = \frac{-4 \pm \sqrt{4^2 - 4(1)(1)}}{2(1)}$$

**Step 3:** Calculate
$$x = \frac{-4 \pm \sqrt{16 - 4}}{2}$$

$$x = \frac{-4 \pm \sqrt{12}}{2}$$

$$x = \frac{-4 \pm 2\sqrt{3}}{2}$$

$$x = \frac{-4}{2} \pm \frac{2\sqrt{3}}{2}$$

$$x = -2 \pm \sqrt{3}$$

**Two solutions:**

$$x_1 = -2 + \sqrt{3} \approx -0.27$$

$$x_2 = -2 - \sqrt{3} \approx -3.73$$

**Answer:** $x = -2 + \sqrt{3}$ or $x = -2 - \sqrt{3}$

---

## Method 2: Factoring (When Possible)

**Process:**
1. Factor the quadratic into two binomials
2. Set each factor equal to zero
3. Solve for $x$

**Formula:**
$$ax^2 + bx + c = (px + q)(rx + s)$$

---

### Example 4: $x^2 + 5x + 6 = 0$

**Step 1:** Find two numbers that:
- **Multiply** to give $c = 6$
- **Add** to give $b = 5$

Numbers: **2** and **3** (because $2 \times 3 = 6$ and $2 + 3 = 5$)

**Step 2:** Factor
$$x^2 + 5x + 6 = (x + 2)(x + 3) = 0$$

**Step 3:** Set each factor to zero
$$(x + 2) = 0 \quad \text{or} \quad (x + 3) = 0$$

**Step 4:** Solve
$$x = -2 \quad \text{or} \quad x = -3$$

**Answer:** $x = -2$ or $x = -3$

---

### Example 5: $x^2 - 5x + 6 = 0$

**Step 1:** Numbers that multiply to $6$ and add to $-5$?
- $-2$ and $-3$ (because $-2 \times -3 = 6$ and $-2 + (-3) = -5$)

**Step 2:** Factor
$$x^2 - 5x + 6 = (x - 2)(x - 3) = 0$$

**Step 3:** Set to zero
$$x - 2 = 0 \quad \text{or} \quad x - 3 = 0$$

**Step 4:** Solve
$$x = 2 \quad \text{or} \quad x = 3$$

**Answer:** $x = 2$ or $x = 3$

---

### Example 6: $x^2 - 9 = 0$ (Difference of Squares)

**Pattern:** $a^2 - b^2 = (a + b)(a - b)$

$$x^2 - 9 = x^2 - 3^2 = (x + 3)(x - 3) = 0$$

$$x + 3 = 0 \quad \text{or} \quad x - 3 = 0$$

$$x = -3 \quad \text{or} \quad x = 3$$

**Answer:** $x = -3$ or $x = 3$

---

## Method 3: Completing the Square

**Process:** Convert to perfect square form: $(x + p)^2 = q$

---

### Example 7: $x^2 + 6x + 5 = 0$

**Step 1:** Move constant to right
$$x^2 + 6x = -5$$

**Step 2:** Take half of $b$, square it, add to both sides
$$\left(\frac{6}{2}\right)^2 = 3^2 = 9$$

$$x^2 + 6x + 9 = -5 + 9$$

**Step 3:** Factor left side (perfect square)
$$(x + 3)^2 = 4$$

**Step 4:** Take square root of both sides
$$x + 3 = \pm 2$$

**Step 5:** Solve
$$x + 3 = 2 \quad \text{or} \quad x + 3 = -2$$

$$x = -1 \quad \text{or} \quad x = -5$$

**Answer:** $x = -1$ or $x = -5$

---

## Method 4: Graphing

**Concept:** Solutions are where graph crosses x-axis

**Parabola equation:** $y = ax^2 + bx + c$

**Vertex form:** $y = a(x - h)^2 + k$

Where $(h, k)$ is the vertex

**Vertex formula:**
$$h = \frac{-b}{2a}$$

Then substitute $h$ into equation to find $k$

---

# 🔍 The Discriminant

**Formula:**
$$\boxed{\Delta = b^2 - 4ac}$$

**Tells us about solutions:**

### Case 1: $\Delta > 0$ (Positive)
- **Two different real solutions**
- Graph crosses x-axis twice

**Example:** $x^2 - 5x + 6 = 0$
$$\Delta = (-5)^2 - 4(1)(6) = 25 - 24 = 1 > 0$$
Solutions: $x = 2$ or $x = 3$ ✓

---

### Case 2: $\Delta = 0$ (Zero)
- **One repeated real solution** (double root)
- Graph touches x-axis once (vertex on x-axis)

**Example:** $x^2 + 4x + 4 = 0$
$$\Delta = 4^2 - 4(1)(4) = 16 - 16 = 0$$
$$(x + 2)^2 = 0$$
Solution: $x = -2$ (repeated) ✓

---

### Case 3: $\Delta < 0$ (Negative)
- **No real solutions** (two complex solutions)
- Graph doesn't touch x-axis

**Example:** $x^2 + 2x + 5 = 0$
$$\Delta = 2^2 - 4(1)(5) = 4 - 20 = -16 < 0$$
No real solutions ✓

---

# 📊 Sum and Product of Roots

If $\alpha$ and $\beta$ are roots of $ax^2 + bx + c = 0$:

**Sum of roots:**
$$\boxed{\alpha + \beta = \frac{-b}{a}}$$

**Product of roots:**
$$\boxed{\alpha \times \beta = \frac{c}{a}}$$

---

### Example 8: $x^2 + 5x + 6 = 0$

**Given:** $a = 1$, $b = 5$, $c = 6$

**Sum of roots:**
$$\alpha + \beta = \frac{-5}{1} = -5$$

**Product of roots:**
$$\alpha \times \beta = \frac{6}{1} = 6$$

**Verify:** Roots are $-2$ and $-3$
- Sum: $-2 + (-3) = -5$ ✓
- Product: $(-2) \times (-3) = 6$ ✓

---

# 🎯 Practice Problems

## Easy Level

### Problem 1: $x^2 - 4 = 0$
<details>
<summary>Show Solution</summary>

**Method:** Difference of squares
$$x^2 - 4 = (x + 2)(x - 2) = 0$$

**Answer:** $x = 2$ or $x = -2$
</details>

---

### Problem 2: $x^2 + 7x + 10 = 0$
<details>
<summary>Show Solution</summary>

**Method:** Factoring (find numbers that multiply to 10, add to 7)
$$x^2 + 7x + 10 = (x + 2)(x + 5) = 0$$

**Answer:** $x = -2$ or $x = -5$
</details>

---

## Medium Level

### Problem 3: $2x^2 + 5x - 3 = 0$
<details>
<summary>Show Solution</summary>

**Method:** Quadratic formula
- $a = 2$, $b = 5$, $c = -3$

$$x = \frac{-5 \pm \sqrt{25 - 4(2)(-3)}}{2(2)}$$

$$x = \frac{-5 \pm \sqrt{25 + 24}}{4}$$

$$x = \frac{-5 \pm \sqrt{49}}{4} = \frac{-5 \pm 7}{4}$$

$$x_1 = \frac{-5 + 7}{4} = \frac{2}{4} = \frac{1}{2}$$

$$x_2 = \frac{-5 - 7}{4} = \frac{-12}{4} = -3$$

**Answer:** $x = \frac{1}{2}$ or $x = -3$
</details>

---

### Problem 4: $x^2 - 6x + 9 = 0$
<details>
<summary>Show Solution</summary>

**Method:** Perfect square
$$x^2 - 6x + 9 = (x - 3)^2 = 0$$

$$x - 3 = 0$$

**Answer:** $x = 3$ (double root)

**Check discriminant:** $\Delta = 36 - 36 = 0$ ✓
</details>

---

## Hard Level

### Problem 5: $3x^2 - 2x - 5 = 0$
<details>
<summary>Show Solution</summary>

**Method:** Quadratic formula
- $a = 3$, $b = -2$, $c = -5$

$$x = \frac{-(-2) \pm \sqrt{(-2)^2 - 4(3)(-5)}}{2(3)}$$

$$x = \frac{2 \pm \sqrt{4 + 60}}{6}$$

$$x = \frac{2 \pm \sqrt{64}}{6} = \frac{2 \pm 8}{6}$$

$$x_1 = \frac{2 + 8}{6} = \frac{10}{6} = \frac{5}{3}$$

$$x_2 = \frac{2 - 8}{6} = \frac{-6}{6} = -1$$

**Answer:** $x = \frac{5}{3}$ or $x = -1$
</details>

---

### Problem 6: $x^2 + 4x + 8 = 0$
<details>
<summary>Show Solution</summary>

**Check discriminant first:**
$$\Delta = 16 - 4(1)(8) = 16 - 32 = -16 < 0$$

**No real solutions!** (Discriminant is negative)

**Complex solutions:**
$$x = \frac{-4 \pm \sqrt{-16}}{2} = \frac{-4 \pm 4i}{2} = -2 \pm 2i$$

**Answer:** No real solutions (or $x = -2 \pm 2i$ in complex numbers)
</details>

---

# 💻 Try in Genius AI!

**Open http://localhost:3000 and ask:**

### Basic:
```
Solve x^2 + 3x - 10 = 0 using the quadratic formula. Show every step with LaTeX formatting.
```

### Intermediate:
```
Solve 2x^2 - 8x + 6 = 0 using two different methods (factoring and quadratic formula). Show both solutions match.
```

### Advanced:
```
For the equation 3x^2 - 7x + 2 = 0:
1. Find the discriminant
2. Determine the nature of roots
3. Solve using quadratic formula
4. Find sum and product of roots
5. Verify your answers
Show all work in LaTeX.
```

### Word Problem:
```
A rectangle's length is 3cm more than its width. If the area is 40 cm², find the dimensions. Set up and solve the quadratic equation with all steps shown.
```

---

# ✨ Why Use Genius AI for Quadratics?

✅ **Beautiful LaTeX** - All formulas rendered perfectly
✅ **Step-by-step** - Every calculation shown clearly
✅ **Multiple methods** - Learn different approaches
✅ **Detailed explanations** - Understand the "why"
✅ **Verification** - Check your answers
✅ **100% FREE** - Unlimited math help

**Your complete quadratic equations guide!** 📐✨🎓
