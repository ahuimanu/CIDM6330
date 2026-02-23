# FOUNDATION 1 VIDEO NARRATION SCRIPT
Patrick Perez | CIDM 6330 | Spring 2026

---

## SEGMENT 1: THE HEADLINE (2–3 minutes)

**[OPEN: Show Foundation1 folder structure on screen]**

"I'm Patrick, and for Foundation 1, I built a data pipeline and problem discovery around hardware OEM decision-making, using Federal Reserve Economic Data—specifically six series from the FRED API.

**[Navigate to FRED_fetch.py and FRED_helper.py, let them appear]**

Here's what I submitted: Two scripts—a fetch module and a helper—that pull six specific economic series from FRED. They live in my project and actually work. I can run them, and they download data."

**[Show combined.csv or one of the individual CSV files in fred_data folder]**

"This is what came out: six time series, joined on date. CPI, semiconductor production, federal funds rate, industrial production, consumer sentiment, and disposable income. Monthly data going back to the 1940s in some cases.

Now, here's the critical part: the domain observation that makes this dataset *matter*.

**[Navigate to PROBLEM_SPACE.md on screen]**

In the hardware industry—Dell, HP, Lenovo—there's a thing I call the 'Hardware Lag.' Decisions made today about component procurement and factory allocation don't hit the market for 3 to 6 months. So economic shifts—like interest rate hikes or semiconductor production dips—they act as *early warning signals* before they show up in quarterly earnings.

I noticed that while Consumer Sentiment is volatile month-to-month, the Producer Price Index shows stickier, long-term trends that directly impact profit margins. That's not obvious. That's domain knowledge.

**[Show the four candidate problems]**

So I surfaced four specific problems that actually exist in this space:

First, 'The Margin Protector'—how can a manufacturer protect margins when the cost to build spikes? Monitor PPI for electronic computer manufacturing, and if component costs trend up by more than 5% over two quarters while MSRP stays flat, margins are at risk.

Second, 'The Capital Cost Forecast'—will Fortune 500 clients delay their 3-year laptop refresh due to high interest rates? A high federal funds rate increases the cost of capital, so CFOs want to 'sweat the assets'—make old laptops last longer. That's a prediction problem.

Third, 'Supply Chain Shortage Scout'—how do we avoid stockouts during semiconductor dips? Industrial production of semiconductors acts as a 3-to-6-month leading indicator for hardware availability.

And fourth, 'The Tier Shifter'—should we manufacture more budget units or premium workstations? Track consumer sentiment and disposable income. If sentiment crashes, consumers trade down to entry-level.

Most datasets in the pool are either finance-focused or infrastructure-focused. I wanted something that could serve a *specific, real role*—something available to planning teams before they see it in their own sales numbers. And I built the dataset specifically to create that tension."

---

## SEGMENT 2: CHARACTERISTICS AND TRADE-OFFS DRIVEN BY THE PROBLEM SPACE (3–4 minutes)

**[Open PROBLEM_SPACE.md, then ARCH_CHAR.md on screen]**

"Here's the key insight: the characteristics I surfaced aren't abstract. They come *directly* from the problems I identified.

Take the 'Margin Protector' and 'Capital Cost Forecast' problems. Both require a CFO to make a $50 million capital decision based on a recommendation from this system—like 'delay your laptop refresh for 18 months because interest rates are high.' That immediately creates an **Auditability** requirement. They need proof. They need a timestamped audit trail showing exactly which data version, which FRED API response, was available when the system made that call.

But here's the second characteristic, **Data Integrity**—specifically consistency in treatment and measurement across six heterogeneous sources. Remember from earlier: some series come seasonally adjusted from FRED, others don't. Some start in 1954, others in 1978. If I standardize everything to the most recent common date and apply uniform adjustments, I gain consistency. But I lose 24 years of historical depth that could tell an important story about interest rates and capital cycles.

Now here's where it gets tight: If I prioritize Auditability—keeping every version, every adjustment decision timestamped—then I have to document *why* I made each integrity choice. That creates audit overhead. If I prioritize Data Integrity through aggressive standardization and truncation to clean dates, I sacrifice the historical context that makes this dataset architecturally interesting in the first place.

So I've hit a real trade-off. I can maintain historical depth and accept inconsistency in how I document it, or I can guarantee consistency and lose decades of usable data.

**[Point to ARCH_CHAR.md]**

That's why those two characteristics are my strongest.

What I *cannot* assess yet—and I'm honest about this in my doc—is **Deployment** and **Cost** characteristics. Because here's what I don't know: Is this a real-time dashboard for traders, which means continuous compute, or a weekly PDF report for executive briefings, which is super low-cost? Those are *fundamentally* different architectures. One scales horizontally with concurrent users. The other is batch. I can't decide the architecture until I understand the use case better."


---

## SEGMENT 3: THE CASE AGAINST YOUR CHOICES (1–2 minutes)

**[Close ARCH_CHAR.md, navigate to PROBLEM_SPACE.md]**

"Let me argue against myself.

First: **Why a different dataset?** The most honest critique I have is that general economic data, even six series, might be too *noisy* for the hardware OEM use case. Semiconductor production is national. Dell is global. I'm using US interest rates to predict enterprise refresh cycles, but the enterprise that matters is in the EU or Asia. Someone could say, 'You're trying to model global supply chains with a single-country lens,' and they'd have a real point.

A stronger dataset might be something more specific—like actual semiconductor fab utilization, or container shipping rates, or something with direct supply-chain granularity. I picked FRED because it was *available* and *interesting*, but not because it was the most architecturally rigorous choice.


Second: Which problem is the weakest architecturally? Honestly, it's **'The Tier Shifter'**—the idea that I can monitor consumer sentiment and disposable income to recommend shifting production from budget to premium units.

Here's why that's weak: The correlation between consumer sentiment and product mix is probably too loose. A hardware OEM doesn't wake up and retool factories based on the University of Michigan consumer sentiment index moving up 2 points. That's a nice data point, but it doesn't force an interesting architectural decision because the business logic is too indirect. There's no triggering event, no clear threshold, no auditability requirement.

Compare that to **'The Margin Protector'** or **'The Capital Cost Forecast'**—those have clear thresholds, are time-bound, and have real business stakes. Those would actually shape the architecture.

Finally: 'This dataset isn't rich enough for a semester project.' How do I respond?

Fair point. But I'm not building a *data science* project. I'm building an *architecture* project. I'm using this data to discover architectural characteristics and constraints. A weak dataset that forces me to make hard decisions about inconsistency and data quality is actually richer architecturally than a mega-dataset that you just throw at a model."

---

## SEGMENT 4: AI COLLABORATION (1–2 minutes)

**[Open AI_LOG.md on screen]**

**[Point to the first section]**

"I asked Claude to help me compare BTS, BLS, and FRED—three different US economic data sources. I could have Googled that, but it was faster to get a structured comparison. I used that. No problem there.

I also asked it to refine my problem space. I gave it a rough idea—'I want to model hardware OEM strategy'—and it came back with four specific business cases. I *modified* the hell out of those.

**[Point to 'Modified' section]**

The AI suggested general financial cases. I pushed back and said, 'No, I want to be specific to Dell, HP, Lenovo.' That's where the hardware OEM angle came from. The AI didn't generate that because I forced domain specificity.

I asked it to build a FRED fetch script and helper. It gave me a template. **[Point to the actual scripts on screen]** This is what I edited and refined. The logic is mine—I had to think about error handling, about where to load the API key, about joining the data correctly. I didn't just run what it generated.

**[Look at one specific thing]**

Here's where I rejected AI guidance: The AI suggested building a generic, highly flexible 'Series Ingester' that could handle any FRED ID dynamically. It's elegant, and in theory, it's the right answer. But I went with a simpler, hard-coded list of six series. Why? Because premature flexibility adds complexity that I don't yet need. I made that call consciously.

And what do I do differently in Foundation 2?

I'm going to use AI to *stress-test* my problem statement, not to *generate* it. I want to ask it harder questions: 'What's missing from my understanding?' 'Where could my assumptions fail?' Rather than 'can you write code for me?'"

---

## CLOSING STATEMENT (15–30 seconds)


"Here's what I understand well after Foundation 1:

The relationship between data characteristics and architectural decisions. I picked six economic series not because they're the most complete dataset, but because they create real tensions—between timeliness and auditability, between flexibility and simplicity. Those tensions will *force* architectural choices in Foundation 2.

One thing I'm least confident about:

Whether the hardware OEM domain is interesting enough, or whether I'm forcing a domain onto data that was meant to be general. I'll know more once I try to build the system and see if it actually *answers* the questions I set it up to answer."

---

## PRODUCTION NOTES

### Screen Navigation Order
1. Foundation1 folder structure (file tree)
2. FRED_fetch.py (quick scan)
3. FRED_helper.py (point out get_api_key, get_fred_series, error handling)
4. fred_data/combined.csv (show a few rows of actual data)
5. ARCH_CHAR.md (read through, especially tensions section)
6. PROBLEM_SPACE.md (point to the four candidates)
7. AI_LOG.md (read through your modifications)

