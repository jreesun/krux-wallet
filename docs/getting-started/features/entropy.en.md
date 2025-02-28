
## Why Does Krux Say the Entropy of My Fifty Dice Rolls Does Not Contain 128 Bits of Entropy?
We want Krux to help users understand the concepts involved in the process, present statistics and indicators, and encourage users to experiment and evaluate results. This way, users learn about best practices in key generation. Below, we delve deeper into the concepts of entropy to better support users' knowledge of sovereign self-custody.

## Entropy in Dice Rolls

Rolling dice and collecting the resulting values can be an effective method for generating cryptographic keys due to the inherent randomness and unpredictability of each roll. Each roll of a die produces a random number within a specific range, and when multiple rolls are combined, they create a sequence that is difficult to predict or reproduce. This sequence can be used to generate cryptographic keys that are robust against attacks. By ensuring that the dice rolls are conducted in a controlled and secure environment, and by using a sufficient number of rolls to achieve the desired level of randomness, one can create cryptographic keys that are highly secure and resistant to brute-force attacks or other forms of cryptanalysis.

### Entropy Definitions

Entropy, a fundamental concept in various scientific disciplines, is most commonly associated with a state of disorder, randomness, or uncertainty within a system. We use the concepts from [thermodynamics entropy](https://en.wikipedia.org/wiki/Entropy_(classical_thermodynamics)), [Shannon's entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)), and [cryptographic entropy](https://en.wikipedia.org/wiki/Entropy_(computing)).

- **Thermodynamics entropy** deals with heat and work. It describes how energy is distributed among the particles in a system, reflecting the system's tendency towards equilibrium and maximum disorder.

- **Shannon's entropy**, from information theory, measures the uncertainty or information content in a message or data source. It quantifies the average amount of information produced by a stochastic source of data, indicating how unpredictable the data is.

- **Cryptographic entropy**, crucial in security, refers to the unpredictability and randomness required for secure cryptographic keys and processes. High cryptographic entropy ensures that keys are difficult to predict or reproduce, providing robustness against attacks.

While thermodynamics entropy deals with physical systems, Shannon's entropy focuses on information content, and cryptographic entropy emphasizes security through randomness.

### Measuring Dice Rolls Entropy
Entropy is a theoretical measure and is not directly measurable from a single roll but rather from the probability distribution of outcomes over many rolls. We can use Shannon's formula for theoretical and empirical calculations. Entropy $S$ can be quantified with:

$$
S = -\sum_{i=1}^{n} p_i \log(p_i)
$$

1. **Empirical Measurement:**
   - Roll the dice a large number of times to observe the frequency of each outcome.
   - Estimate the probabilities $p_i$ based on observed frequencies.

2. **Theoretical Calculation:**
   - Use the uniform distribution assumption (equal probability for all outcomes).

where:
- $p_i$ is the probability of each possible outcome (or state) of the system.
- $n$ is the number of possible outcomes.

## Empirical (Real) vs. Theoretical Entropy in Dice Rolls

When calculating the entropy of dice rolls, the difference between real and theoretical results arises from the assumption of perfect fairness and uniformity versus the inherent imperfections in real-world experiments.

### Theoretical Entropy

The theoretical entropy calculation assumes that the dice are perfectly fair, meaning each face has an equal probability of landing face up.

Consider a fair six-sided die. The possible outcomes when rolling one die are {1, 2, 3, 4, 5, 6}, each with an equal probability of $\frac{1}{6}$.

1. **Single Die Roll:**
   - Each outcome has a probability $p_i = \frac{1}{6}$.
   - The entropy $S$ for one die roll is calculated as:

$$
S = - \sum_{i=1}^{6} \left( \frac{1}{6} \log_2 \left( \frac{1}{6} \right) \right)
$$

   Since $`\log_2(1/6) = -\log_2(6)`$ :

$$
S = -6 \left( \frac{1}{6} \times -\log_2(6) \right) = \log_2(6) \approx 2.585 \text{ bits}
$$

2. **Multiple Dice Rolls:**
   - For multiple dice, the entropy increases as the number of possible outcomes increases. For $k$ fair dice, the number of possible outcomes is $6^k$.
   - The entropy $S$ for $k$ dice is:

     $S = \log_2(6^k) = k \log_2(6) \approx 2.585k \text{ bits}$

   - For example, entropy for the roll of 50 fair dice is calculated as:

     $S = \log_2(6^{50}) = 50 \log_2(6) \approx 2.585 \times 50 \approx 129.25 \text{ bits}$

   This calculation assumes that every outcome (each face of the die) has an equal likelihood, leading to a uniform distribution.

### Empirical Entropy

In a real sample of dice rolls, several factors can cause deviations from the perfect uniform distribution:

1. **Imperfect Dice**: Real dice may not be perfectly balanced. Small manufacturing defects can make certain faces slightly heavier or lighter, causing biases.
2. **Rolling Conditions**: The way the dice are rolled, the surface they land on, and even air currents can introduce slight biases.
3. **Finite Sample Size**: When rolling dice a finite number of times, the observed frequencies of each face will naturally deviate from the expected uniform distribution due to random variations. This phenomenon is more pronounced with smaller sample sizes.

When you roll a die multiple times and observe the outcomes, you can calculate the empirical probabilities $p_i$ of each face. Using these probabilities, the entropy is calculated as:

$$
S = - \sum_{i=1}^{6} p_i \log_2(p_i)
$$

### Example


Suppose you roll a six-sided die 50 times and get the following results:

- 1: 4 times
- 2: 9 times
- 3: 7 times
- 4: 10 times
- 5: 12 times
- 6: 8 times

We can calculate Shannon's entropy as follows:

#### Step 1: Calculate Probabilities

Total number of rolls:

$$
N = 4 + 9 + 7 + 10 + 12 + 8 = 50
$$

Probabilities for each outcome:

$$
p_1 = \frac{4}{50} = 0.08 
$$

$$
p_2 = \frac{9}{50} = 0.18 
$$

$$
p_3 = \frac{7}{50} = 0.14 
$$

$$
p_4 = \frac{10}{50} = 0.2 
$$

$$
p_5 = \frac{12}{50} = 0.24 
$$

$$
p_6 = \frac{8}{50} = 0.16 
$$

#### Step 2: Compute Entropy

Using Shannon's entropy formula:

$$
S = -\sum_{i=1}^{n} p_i \log_2(p_i)
$$

Calculate each term:

$$
S_1 = -p_1 \log_2(p_1) = -0.08 \log_2(0.08) = -0.08 \times (-3.64386) = 0.291509
$$

$$
S_2 = -p_2 \log_2(p_2) = -0.18 \log_2(0.18) = -0.18 \times (-2.47393) = 0.445307
$$

$$
S_3 = -p_3 \log_2(p_3) = -0.14 \log_2(0.14) = -0.14 \times (-2.8365) = 0.39711
$$

$$
S_4 = -p_4 \log_2(p_4) = -0.2 \log_2(0.2) = -0.2 \times (-2.32193) = 0.464386
$$

$$
S_5 = -p_5 \log_2(p_5) = -0.24 \log_2(0.24) = -0.24 \times (-2.05889) = 0.494132
$$

$$
S_6 = -p_6 \log_2(p_6) = -0.16 \log_2(0.16) = -0.16 \times (-2.64386) = 0.423018
$$

Sum the contributions:

$$
S = S_1 + S_2 + S_3 + S_4 + S_5 + S_6 
$$

$$
S = 0.291509 + 0.445307 + 0.39711 + 0.464386 + 0.494132 + 0.423018 = 2.515462
$$

Thus, the Shannon's entropy for the given distribution of dice rolls is approximately $2.52$ bits per roll.

This will give you a different value than $\log_2(6)$ due to the deviations in the empirical probabilities.

The total entropy for the $N = 50$ rolls is:

$$
S_{total} = S \times N = 2.515 + 50 \approx 125.8 \text{ bits}
$$

#### Shannon's Entropy in Practice

Calculating Shannon's entropy on a real sample of dice rolls provides insights into the actual randomness and fairness of the dice and rolling conditions. Deviations from the theoretical entropy reflect the natural imperfections and variances inherent in real-world scenarios. This understanding helps in evaluating and improving the fairness and randomness of dice or similar systems.

Shannon's entropy evaluates the statistical probability distribution of samples of a dice roll. An even distribution results in higher entropy, closer to the theoretical maximum entropy, which assumes perfectly distributed rolls. An uneven distribution, created, for example, by a biased die, will result in lower Shannon's entropy. In an extreme case, with a terribly biased die that always lands on the same side, Shannon's entropy will be zero.

## Cryptographic Entropy

Shannon's entropy, while a powerful measure of information content and uncertainty in a statistical distribution for natural samples, is not considered cryptographic entropy due to its inability to detect patterns or other sources of predictability within data. Shannon's formula quantifies the average information produced by a stochastic process, essentially measuring the expected surprise in a sequence of symbols based on their probabilities. However, it does not account for potential structure, correlations, or regularities within the data that could be inserted by a user and exploited by an attacker.

Cryptographic entropy, on the other hand, requires a higher standard of unpredictability. It must ensure that every bit of the cryptographic key is as random and independent as possible, making it resilient against any form of analysis that could reveal patterns or reduce the effective randomness. While Shannon's entropy can evaluate the statistical distribution of symbols, it falls short in guaranteeing the absence of patterns or dependencies, which are crucial for maintaining the security of cryptographic systems. Thus, cryptographic entropy encompasses a broader concept of randomness, ensuring that the generated keys are not only statistically random but also free from any detectable structure or predictability.

### Pattern Detection

It is possible to have dice rolls with an even distribution but poor cryptographic entropy. This issue arises when patterns are present in the sequences. Examples include sequences like 123456123456123..., 111122223333..., and 654321654321..., which exhibit poor cryptographic entropy despite having even distribution and high Shannon's entropy.

To mitigate this issue, Krux has implemented a pattern detection algorithm that evaluates the Shannon's entropy of the rolls' derivatives. In practice, this algorithm detects arithmetic progression components in the dice rolls and raises a warning if a certain threshold is crossed.

## What Krux Does?

- Krux requires a minimum number of rolls based on theoretical entropy.
- Krux warns the user if low Shannon's entropy, calculated with the actual rolls, is detected.
- Krux warns the user if it suspects there are patterns within the actual rolls.

## Conclusion

While Krux cannot ensure rolls have good or bad cryptographic entropy, it does provide indicators to help users detect issues and learn about the concepts involved in mnemonic generation.
