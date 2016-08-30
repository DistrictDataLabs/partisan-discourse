# Partisan Discourse

**A web application that identifies party in political discourse and an example of operationalized machine learning.**

[![Build Status][travis_img]][travis_href]
[![Coverage Status][coveralls_img]][coveralls_href]
[![Stories in Ready][waffle_img]][waffle_href]

[![Political Parties](docs/img/partisan.jpg)][partisan.jpg]

## About

This small web application is intended to highlight how to operationalize machine learning models in a web application. Through the lens of a political classifier we see how models can be managed and stored inside of Django for per-user and global modeling.

### Attribution

The image used in this README, [Partisan Fail][partisan.jpg] by [David Colarusso](https://www.flickr.com/photos/dcolarusso/) is licensed under [CC BY-NC 2.0](https://creativecommons.org/licenses/by-nc/2.0/)

## Changelog

The release versions that are deployed to the web servers are also tagged in GitHub. You can see the tags through the GitHub web application and download the tarball of the version you'd like.

The versioning uses a three part version system, "a.b.c" - "a" represents a major release that may not be backwards compatible. "b" is incremented on minor releases that may contain extra features, but are backwards compatible. "c" releases are bug fixes or other micro changes that developers should feel free to immediately update to.

### Version 0.2 Beta 3

* **tag**: [v0.2b3](https://github.com/DistrictDataLabs/partisan-discourse/releases/tag/v0.2b3)
* **deployment**: Monday, August 29, 2016
* **commit**: [see tag](#)

This is an intermediate release to ensure that some front end components become visible in advance of the first release. In particular the annotation help button on the document view and the about page that gives built with attribution. This release also fixes the "." in usernames bug that would not allow people to log in or access their profile.

This release also contains components that are not officially ready but sit quietly in the background waiting to be deployed. This includes the management command to build models, the corpus object to link data sets, estimator models for Scikit-Learn pipeline/estimator data storage and more. These elements will be discussed in detail in future releases. 

### Version 0.1 Beta 1

* **tag**: [v0.1b1](https://github.com/DistrictDataLabs/partisan-discourse/releases/tag/v0.1b1)
* **deployment**: Monday, July 18, 2016
* **commit**: [393211a](https://github.com/DistrictDataLabs/partisan-discourse/commit/393211acd1a270e04ae7b69f750be2f3e7305230)

This is the first beta release of the Partisan Discourse application. Right now this simple web application allows users to sign in, then add links to go fetch web content to the global corpus. These links are then preprocessed using NLP foo. Users can tag the documents as Republican or Democrat, allowing us to build a political classifier.

<!-- References -->
[travis_img]: https://travis-ci.org/DistrictDataLabs/partisan-discourse.svg
[travis_href]: https://travis-ci.org/DistrictDataLabs/partisan-discourse
[waffle_img]: https://badge.waffle.io/DistrictDataLabs/partisan-discourse.png?label=ready&title=Ready
[waffle_href]: https://waffle.io/DistrictDataLabs/partisan-discourse
[coveralls_img]: https://coveralls.io/repos/github/DistrictDataLabs/partisan-discourse/badge.svg?branch=master
[coveralls_href]:https://coveralls.io/github/DistrictDataLabs/partisan-discourse?branch=master
[partisan.jpg]: https://flic.kr/p/a3bXVU
