# YouTube Discussion Tree API 

[![Build Status](https://travis-ci.com/quimpm/youtube_discussion_tree.svg?branch=main)](https://travis-ci.com/quimpm/youtube_discussion_tree)[![Coverage Status](https://coveralls.io/repos/github/quimpm/youtube_discussion_tree/badge.svg)](https://coveralls.io/github/quimpm/youtube_discussion_tree)[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](http://opensource.org/licenses/MIT)[![image](https://img.shields.io/pypi/v/youtube-discussion-tree-api.svg)](https://pypi.org/project/youtube-discussion-tree-api/) [![image](https://img.shields.io/pypi/pyversions/youtube-discussion-tree-api.svg)](https://pypi.org/project/youtube-discussion-tree-api/)

This is a python API that allows you to obtain the discussion 
that occurs in the comments of a YouTube video as a tree structure.
It also controls the quota usage that consumes your implementation over
YouTube Data API through this library, and allows you to represent and 
serialize the discussion tree.

## Install

It is recommended to install it through pip:


```bash
pip install youtube_discussion_tree_api
```

Also, if you want to use it from source you will have to install manually the dependencies:

```bash
pip install -r requeriments.txt
```

## API

Now we're going to dive into the features that the API provide and how to use them.

### Generating a tree

This is the main feature of the API. The easiest way of generating a tree is:

```python
from youtube_discussion_tree_api import YoutubeDiscussionTreeApi

api = YoutubeDiscussionTreeApi("<put your gcs api and services api key>")
tree = api.generateTree("put the videoId")

```

First, you create a YoutubeDiscussionTreeApi object with the API KEY of your GCP project. This object
is thought as the template object that holds all the interactions with the YouTube Data API.

Then, we call the method generateTree, that give us as a response a YoutubeDiscussionTree object that
holds the tree structure.

Each node of the tree is a Node object:

```python
class Node:
    id: int
    author_name: str
    author_id: int
    text: str
    like_count: int
    parent_id: int
    published_at : str

```
The **root** node represents the video. In the text field of the root Node, a transcription of the whole video is provided. 
The API can only generate trees of the videos that have manual or auto-generated English subtitles.

The method generateTree has two optional parameters that are:
* sumarization -> bool: This parameter is for applying a summarization to the transcription of the video.
* conflict_solving_algorithm -> function: This parameter is a function that does the resolution of conflicts that we face when generating the tree. Will be explained later.

We can get the list of all the nodes of our tree by doing:

```python
tree.get_nodes()
```

### Serializing a tree

We can serialize our tree into a xml file:

```python
tree.serialize("outuput_file.xml")
```

This will construct a xml file with the following structure:

```xml
<entailment-corpus num_edges="162" num_nodes="163">
    <argument-list>
        ...
    <argument-list>
    <argument-pairs>
        ...
    <argument-pairs>
</entailment-corpus>

```
In argument-list component there will be all the comment nodes with some information of the Node objects. 
In the argument-pairs component, there will be all the edges that communicate the nodes described in the previous component.

A node will be represented as:

```xml
<arg author="Flash Man" author_id="UCeFi97LktRRtpCvi_vqEmfg" id="Ugh8N1Ch9gCr-HgCoAEC" likeCount="1145">
    My dad is an expert dragon slayer. "eeer but I don't see any dragons around... " You're welcome.
</arg>
```

And a pair as:

```xml
<pair id="1">
    <t id="Ugh8N1Ch9gCr-HgCoAEC"/>
    <h id="LnX3B9oaKzw"/>
</pair>
```
Where h is the destination and t the origin

Also, the function serialize() has an optional argument called **aditional_atributes**. You can pass a function that receives a Node object and outputs a {key : value} dictionary  
that will represent the additional attributes that you would like to add to the xml tags that represent the Nodes. The key will be the attribute name and the value will be the value of the attribute. 

```python
def my_additional_atributes(node):
    return {
        "date" : node.publishedAt
        "sentiment" : sentiment_analysis(node.txt) #Imagine we have a function that does sentiment analysis from an input text
    }

tree.serialize("outuput_file.xml", my_aditional_atributes)
```
The nodes will have the following form:

```xml
<arg author="Flash Man" author_id="UCeFi97LktRRtpCvi_vqEmfg" id="Ugh8N1Ch9gCr-HgCoAEC" likeCount="1145" date="12-12-2012" sentiment="NEGATIVE">
    My dad is an expert dragon slayer. "eeer but I don't see any dragons around... " You're welcome.
</arg>

```

### Representing a tree

If you want to see a representation of the tree, you can do:

```
tree.show()
```
And this will output a tree like:
```
LnX3B9oaKzw
├── Ugg06_f0qAVH6HgCoAEC
├── Ugg662Arr0neQXgCoAEC
│   ├── Ugg662Arr0neQXgCoAEC.8LvCxcl0tY18LvI0OyzxUW
│   ├── Ugg662Arr0neQXgCoAEC.8LvCxcl0tY18LvIRl9v4kU
│   ├── Ugg662Arr0neQXgCoAEC.8LvCxcl0tY18LvIlAkRi3e
                    .
                    .
                    .
```

### Conflict Solving Algorithm

If you read the "Generating a tree" part, you may have seen that in the generateTree function there is an optional
argument for a conflict solving algorithm. Well, lets explain what we define as a conflict.

We say that there is a conflict when a user wants to reply to another user's comment, but this second one
has made more than one contribution previously to the comment thread. This is because YouTube doesn't store 
the reference to the comment of the comment thread that we want to reply. It automatically sets the parent id
of the reply to the top level comment of the comment thread, instead of the id of the comment that we are replying to. 

In order to solve that, in this library there is an implementation of an algorithm that solve this conflicts automatically.
The algorithm it's an implementation of the tf-idf algorithm that selects a candidate from a set of candidates for the 
reply that we don't know to which of this candidate belongs.

In order to make this library as flexible as possible, it's open to accept a function with an implementation of a 
conflict solving  algorithm made by you through the optional argument of generateTree.

This function will receive as parameter the reply Node and a set of Node candidates.

### Search videos 

Through the YoutubeDiscussionTreeAPI object, you can also request for a set of videos that are found matching a given query:

```python
from youtube_discussion_tree_api import YoutubeDiscussionTreeApi

api = YoutubeDiscussionTreeApi("<put your gcs api and services api key>")
videos = api.search_videos("Functional Programming")

```
This will return a set with 5 Video objects:

```python
class Video:
    id: int
    title : str
    description: str
    channel_name: str
    channel_id: str
    published_at : str
```

You can expand or diminish the number of results in the result set by passing another optional parameter: 

```python
from youtube_discussion_tree_api import YoutubeDiscussionTreeApi

api = YoutubeDiscussionTreeApi("<put your gcs api and services api key>")
videos = api.search_videos("Functional Programming", 50)
```

### Quota

Additionally, this library maintains the number of quota that your implementation is consuming against the 
Google YouTube API service. This is because the free service is limited to a quota of 10000 daily. Each tree
generation consumes 2 quota, and each video search consumes 100  quota.

A data object is serialized in a pickle file. You will see that it will appear in the path in which your script 
that uses the library is. It automatically resets its value day after day.

In order to get quota information, you can do:

```python
from youtube_discussion_tree_api import YoutubeDiscussionTreeApi

api = YoutubeDiscussionTreeApi("<put your gcs api and services api key>")
api.quota_info()
```

This will give you a dict like:

```python
{
    "limit" : 10000
    "spent" : <num-expended-quota>
}
```

## Author Note

Hey, Quim here! :man_technologist:

So, this is it for the YouTube Discussion Tree API, hope you enjoy the package! If you have any comment(xD)
on the implementation, or you want to share some features that can be added to de library, hit me up!
Any kind of feedback will be pleasantly accepted! :smile:

Quim10^-12

