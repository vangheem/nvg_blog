---
layout: post
title:  "Why Plone Resource Registries Happened"
date: 2018-09-17 01:30:00
categories: python open-source plone javascript
description: Reflective on what went wrong with resource registries
published: true
---

It all started with the
[2014 Zidandca Sprint](https://plone.org/news/old-news/zidanca-sprint-report-js-less-integration).

We had [the mockup project](https://github.com/plone/mockup). We had [Plone](https://plone.org).
Now, we needed a way to bring to make them work in "harmony" together.

It was the first time I met [Ramon Navarro Bosch](https://twitter.com/bloodbare). Side note: who since then,
I've done a lot of open source work with. I even joined one of his startups.


## The mockup project

The mockup project was a project which aimed to bring modern JavaScript development to the open source Plone
project. It did this by creating a pure JavaScript project which frontend development was done on separate
from the Plone CMS.

Previously in Plone, JavaScript development was coupled with the CMS. You would register your JavaScript
file to be installed onto the site. Then the CMS would concatenate all the JavaScript and CSS files together
and output a set of files that were included in the html of the page.

The idea of mockup was to decouple frontend development from the CMS and to come up to speed with modern JavaScript.


## The problem

Well, decoupling can be great; however, we still need to deliver a CMS. Within the Plone community, it was
understood that you needed to be able to customize and rebuild JavaScript and CSS files within the CMS(I think
now people are not as interested in this feature).

The original author of the mockup project was not interested in merging the world. In fact, if I remember correctly,
I believe his intention was that if people wanted to customize the JavaScript components shipped with Plone,
they should fork the project and make the customizations here.

To give you an idea at the state of JavaScript in 2014, here are the type of components we're talking about:
- Grunt
- Backbone js
- JQuery
- RequireJS
- LESS CSS

(ReactJS was just getting started and we had a few things written in it as well)

What we were asked to solve:
 - integrate mockup within plone
 - add/remove js/css resource
 - customize resources
 - build js/css files

Also keep in mind, we were asked to solve these problems mostly for people who still wanted to do
TTW(through the web) development. Ramon and I did not do TTW development and JavaScript technology
does not jive very well with this idea. In other words, we were asked to solve a problem for which
we had no use-case ourselves.


## Resource registries

From those constraints and the current state of things, we came up with the Plone
[Resource registry](https://docs.plone.org/adapt-and-extend/theming/resourceregistry.html).

Basically, what is does is:

- allow registering "resources" and "bundles"
- a resource is a JavaScript or CSS file
- a bundle is a build which combines files and uses the RequireJS to resolve resource dependencies
- also supports compiling LESS CSS
- support building resources on the command line from configured customizations/registrations


## Retrospective

Well, it didn't work out well. For the most part, either people didn't like it or didn't understand it.
Ramon and I spent a insane amounts of time working out the issues, documenting and training people on it.

"This is a amazing. You integrated JavaScript development with a CMS. No one has ever done that." said
NO ONE EVER about the project.

Summary of the problems:
- Complexity: it was hard to describe the JavaScript dependency chain in configuration and then document/train on that
- JavaScript technology was still new and buying into a bunch of tech early was a mistake
- RequireJS, LESSC, Backbone: now plone is stuck for a while on it
- Buggy and difficult to understand when problems occurred
- Difficult to change development paradigms when people are used to traditional frontend development

One good thing about it is that it forced the community into learning and exploring different approaches
to integrating frontend development with Plone.
