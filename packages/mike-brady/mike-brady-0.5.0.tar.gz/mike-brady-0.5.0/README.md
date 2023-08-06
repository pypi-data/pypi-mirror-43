# Repo Blueprinter

## Overview
The goal of this project is to provide an easy way to create a "repo blueprint template" from which developers can build their own projects. You can create placeholders in the template and populate the values when the new repo is created.

## Features
* Uses the [jinja2](http://jinja.pocoo.org/) template engine for easy and powerful templates
* Limit templated files to specific file types
* Template filenames and folders

## Why not just fork?
Forking is great if you want to potentially merge back with the main project. In this case, we want to provide developers with a basic blueprint, let them fill in their own values, but they won't be merging back into the main project.

## Installation

`$ pip install repo-blueprint`

## Usage
