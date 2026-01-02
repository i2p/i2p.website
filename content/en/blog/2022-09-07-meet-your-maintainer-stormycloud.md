---
title: "Meet Your Maintainer: StormyCloud"
date: 2022-09-07
author: "sadie"
description: "An interview with the maintainers of the StormyCloud Outproxy"
categories: ["general"]
---

## A conversation with StormyCloud Inc.

With the most recent [I2P Java release](https://geti2p.net/en/blog/2022/08/22/1.9.0-Release), the existing outproxy, false.i2p was replaced with the new StormyCloud outproxy for new I2P installs. For people who are updating their router, changing over to the Stormycloud service can be done quickly.

In your Hidden Services Manager, change both Outproxies and SSL Outproxies to exit.stormycloud.i2p and click on the save button at the bottom of the page.

## Who is StormyCloud Inc?

**Mission of StormyCloud Inc.**

To defend Internet access as a universal human right. By doing so, the group protects users' electronic privacy and builds community by fostering unrestricted access to information and thus the free exchange of ideas across borders. This is essential because the Internet is the most powerful tool available for making a positive difference in the world.

**Vision Statement**

To become a pioneer in providing free and open Internet to everyone in the universe because Internet access is a basic human right ([https://stormycloud.org/about-us/](https://stormycloud.org/about-us/))

I met with Dustin to say hello, and to talk more about privacy, the need for services like StormyCloud, and what drew the company to I2P.

**What was the inspiration behind starting StormyCloud?**

It was late 2021, I was on the /r/tor subreddit. There was a person who had responded in a thread about how to use Tor who talked about how they relied on Tor in order to stay in contact with their family. Their family lived in the United States, but at the time they resided in a country where internet access was very restricted. They needed to be very cautious about who they communicated with and what they said. For these reasons, they relied on Tor. I thought about how I can communicate with people without fear or restrictions and that it should be the same for everyone.

The goal of StormyCloud is to help as many people as we can to do that.

**What have been some of the challenges of getting StormyCloud started?**

The cost — it is ungodly expensive. We went the data centre route since the scale of what we are doing is not something that can be done on a home network. There are equipment expenses and reoccurring hosting costs.

In regard to setting up the non-profit, we followed in Emerald Onion's path and utilized some of their documents and lessons learned. The Tor community has many resources available that are very helpful.

**How has the response been to your services?**

In July we served 1.5 billion DNS requests over all of our services. People appreciate that there is no logging being done. The data is just not there, and people like that.

**What is an outproxy?**

An outproxy is similar to Tor's exit nodes, it allows for clearnet (normal internet traffic) to be relayed through the I2P network. In other words, it allows I2P users to access the internet through the safety of the I2P network.

**What is special about the StormyCloud I2P Outproxy?**

To start with we are multi-homed which means we have several servers serving outproxy traffic. This ensures the service is always available to the community. All the logs on our servers are wiped every 15 minutes. This ensures both law enforcement and ourselves do not have access to any data. We support visiting Tor onion links though the outproxy, and our outproxy is pretty fast.

**How do you define privacy? What are some of the issues you see with overreach and data handling?**

Privacy is freedom from unauthorized access. Transparency is important, such as opting in — the example being GDPR requirements.

There are big companies hoarding data that is being used for [warrantless access to location data](https://www.eff.org/deeplinks/2022/08/fog-revealed-guided-tour-how-cops-can-browse-your-location-data). There is overreach of tech companies into what people think is, and should be private, like photos or messages.

It is important to keep doing outreach about how to keep your communication safe, and what tools or apps will help a person do so. The way that we interact with all of the information out there is important as well. We need to trust but verify.

**How does I2P fit into StormyCloud's Mission and Vision Statement?**

I2P is an open source project, and what it offers aligns with the mission of StormyCloud Inc. I2P provides a layer of privacy and protection for traffic and communication, and the project believes that everybody has a right to privacy.

We became aware of I2P in early 2022 when talking to people in the Tor community, and liked what the project was doing. It seemed similar to Tor.

During our introduction to I2P and its capabilities, we saw the need for a reliable outproxy. We had really great support from people in the I2P community to create and start providing the outproxy service.

**Conclusion**

The need for awareness about surveilling what should be private in our online lives is ongoing. Collecting any data should be consensual, and privacy should be implicit.

Where we cannot trust that our traffic or communication will not be observed without consent, we thankfully have access to networks that will by-design anonymize traffic and hide our locations.

Thank you to StormyCloud and everyone who provides outproxies or nodes for Tor and I2P so that people can access the internet more safely when they need to. I look forward to more people bridging the capabilities of these complementary networks to create a more robust privacy ecosystem for everyone.

Learn more about StormyCloud Inc.'s services at [https://stormycloud.org/](https://stormycloud.org/) and help support their work by making a donation at [https://stormycloud.org/donate/](https://stormycloud.org/donate/).
