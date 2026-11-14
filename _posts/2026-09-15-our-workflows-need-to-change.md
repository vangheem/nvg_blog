---
layout: post
title: "Our workflows need to change"
date: 2026-09-15 10:30:00
categories: ai si
description: We're all using Agents wrong.
published: true
---

# What are doing even doing?

For the most part, we are just applying AI/Agents onto old organizational patterns of working. We still do the same types of meetings and organize our work, companies and relationships in the same ways we used to.

For me, that means we still use Jira, Confluence, Github, etc.

What this means in practice is that we're constantly shuffled text to and from agents. Bottom line, a work day consists of:

 - Humans generate text with agents
 - Human(or agent even) then asks a human to review
 - Reviewer Human then asks agent to summarize. Likely because the text outputted by the original agent was way too verbose.
 - Agent responds

What are we doing?!


# "Meat Proxies"

This is the term used by many to describe the behavior we have. For many, their roles really consist of being proxies to the LLMs. Because we're just applying LLMs onto old workflows, we(the "meat" here) become the proxies to the LLMs who actually do the work.

"Meat" is intentionally dehumanizing language because the work and system is dehumanizing when all the thinking and work being done are with the LLM.


# Are we more productive?

Slight digression here but let's think about where LLMs/Agents work and do not work.

Often, we are incredibly more productive for things like:
- Generating reports
- Generating code
- Automating rote tasks
- Research
- Validation

But, there are other areas we struggle:
- Good decision making
- Human review and validation
- Human feedback cycles

For an organization, sometimes the biggest bottleneck is solid decision making. Using LLMs and Agents without care can actually slow things down because of the absolute insane amount of vebosity and jargon it produces. You can appear to be doing a lot of work but just producing work that slow the organization down because it can't make decisions quickly.


# Agent writing is garbage anyways

Well, it's not garbage. Many times, it's quite good.

The problem is, most LLMs can be quite verbose. It probably has to do with how they require text to reason about what they are outputting. So if a user of an LLM is not careful, they will produce content that basically includes all the agent reasoning in it.

Additionally, humans can infer on background/shared knowledge much better than an LLM can obviously.

So... LLM output ends up being incredibly verbose. 1) It doesn't know what to leave out, 2) it doesn't know what it can infer about existing shared knowledge and concepts, and 3) it needs the verbosity for itself in order to keep producing coherent output.

For an organization that wants to move fast and make solid decisions, using LLMs and Agents without care can actually slow things down. You can appear to be doing a lot of work but just producing work that slow the organization down.

For what it's worth, I know this doesn't have to be the case. If you know how to use LLMs and agents, you can coach them on the correct context and the correct way to output so it doesn't overly produce jargon and verbosity.


# What do our workflows look like right now?

Agents should be working for us, not us for them.

Instead of using agents to produce lots of text for us to review because that's what we used to do ourselves, we need to build new organizational systems with agents at different parts of the system instead of having all the human intermediaries.

Let's take an existing example of creating a feature in a big-ole software company:

- Product produces feature definition with help of AI
- UX does designs for feature with AI
- Engineering team sees, extremely verbose feature definition, summarizes it with AI
- Engineering team creates Jira Epic and tickets to split work up with AI
- Individual engineer selects ticket, uses their coding agent to do something like: "Review ticket XYZ, assign it to me, put in progress, implement it with the following specs...Create PR"
- Agent automatically reviews PR
- Another engineer reviews, doesn't fully understands, uses an Agent to summarize and explain parts of the implementation. Approves.
- QA Engineer(maybe this is old org where different team has to write tests) needs to write tests for feature -- does it with an agent
- Feature deploys to production.
- There is an error that is reported. An agent reviews, etc, etc

At basically every layer, this organization kept things exactly the same as they used to but just inserted AI and Agents into the mix and each one of these stages, an LLM was involved.


# What could the future look like?

I think organizations that keep up this approach are going to fail.

We need new ways of working.

We need to cut out all the meat-proxy-to-LLMs business.

We need complete agent closed-loops systems that we interact with to get work done.

No more, meat-proxies.

Maybe that looks something like:

- [Product definition and design system exists]
  - Allows product to research, iterate, test and visualize ideas
- Product produces feature definition
  - This is done completely with agent loop system of refining and design the feature.
  - Maybe a complete prototype is produced
- [Agent coding system Exists]
  - When new feature is ready, agent builds it
  - Before it gets to engineer, it is reviewed across different dimensions for how software should be made for this particular type of system.
- Engineer reviews agent build
  - Interactively, agent takes comments, applies changes, etc
- [Software deployment system exists]
  - Deploys changes to software in production
  - Remediates issues when they come up
  - Notifies humans when things are going wrong

In this picture, you have 2 types of teams:
- Product
- Engineers


In the old version you had:
- product
- ux
- engineering
- testing
- devops/infra/platform/etc
