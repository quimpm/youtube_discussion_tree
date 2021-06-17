# Youtube Discusion Tree API 

This is a python API that allows you to obtain the discusion 
that occurs on the comments of a Youtube video as a tree structure.
It also controls the quota usage that consumes your implementation over
Youtube Data Api through this library, and allows you to represent and 
serialize the discusion tree.

## Install

It is recomended to install it through pip:

```bash
pip install youtube_discusion_tree_api
```

Also, if you want to use it from source you will have to install manually the dependences:

```bash
pip install -r requeriments.txt
```

## API

Now we're going to dive into the features that the API provide and how to use them.

### Generating a tree

This is the main feature of the API. The easyest way of generating a tree is:

```python
from youtube_discusion_tree_api import YoutubeDiscusionTreeApi

api = YoutubeDiscusionTreeApi("<put your gcs api and services api key>")
tree = api.generateTree("put the videoId")

```

First you create a YoutubeDiscusionTreeApi object with the api key of your GCP project. This object
is thought as the template object that holds all the interactions with the Youtuba Data API.

Then, we call the method generateTree, that give us as a response a YoutubeDiscusionTree object that
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
The **root** node represents the video. In the text field of the root node a transcription of the whole video is provided. 
The Api can only generate trees of the videos that have manual or autogenerated english subtitles.

The method generateTree has two optional parameters that are:
* sumarization -> bool: This parameter is for aplying a summarization to the transcription of the video.
* conflict_solving_algorithm -> function: This parameter is a functions that does the resolution of conflicts that we face when generating the tree. Will be explained later.

We can get the list of all the nodes of our tree by doing:

```python
tree.get_nodes()
```

### Serializing a tree

We can serialize our tree into an xml file:

```python
tree.serialize("outuput_file.xml")
```

This will construct an xml file with the following structure:

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
In argument-list component there will be all the comment nodes with some of the information of the Node objects. 
In argument-pairs component there will be all the edges that comunicate the nodes described in the previous component.

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

### Representing a tree

If you want to see a representation of the tree you can do:

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

If you readed the "Generating a tree" part, you may have seen that in the generateTree fucntion there is an optional
argument for a conflict solving algorithm. Well, lets explain what we define as a conflict.

We say that there is a conflict when a user wants to reply to another user's comment, but this second one
has made more than one contribution previously to the comment thread. This is becouse Youtube doesn't store 
the reference to the comment of the comment thread that we want to reply. It automatically sets the parent id
of the reply to the top level comment of the comment thread instead of the id of the comment that we are replying to. 

In order to solve that, in this library there is an implementation of an algorithm that solve this conflicts automatically.
The algorithm it's an implementation of the tf-idf algorithm that selects a candidate from a set of candidates for the 
reply that we don't know to which of this candidate belongs.

In order to make this library as felxible as possible, it's open to accept a function with an implementation of a 
conflict solving  algorithm made by you through the optional argument of generateTree.

This function will recive as parameter the reply Node and a set of Node candidates.

### Search videos 

Through the YoutubeDiscusionTreeAPI object you can also request for a set of viedos that are found matching a given query:

```python
from youtube_discusion_tree_api import YoutubeDiscusionTreeApi

api = YoutubeDiscusionTreeApi("<put your gcs api and services api key>")
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
from youtube_discusion_tree_api import YoutubeDiscusionTreeApi

api = YoutubeDiscusionTreeApi("<put your gcs api and services api key>")
videos = api.search_videos("Functional Programming", 50)
```

### Quota

Aditionally, this library mantains the number of quota that your implementation is consuming against the 
Google Youtube API service. This is becouse the free service is limitated to a quota of 10000 daily. Each tree
generation consumes 2 quota, and each video search consumes 100  quota.

A data object is serialized in a pickle file. You will see that it will apear in the path in wich your script 
that uses the library is. It automatically resets its value day after day.

In order to get quota information you can do:
```python
from youtube_discusion_tree_api import YoutubeDiscusionTreeApi

api = YoutubeDiscusionTreeApi("<put your gcs api and services api key>")
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

So, this is it for the Youtube Discusion Tree API, hope you enjoy the package! If you have any comment(xD)
on the impementation, or you want to share some features that can be added to de library, hit me up!
Any kind of feedback will be pleasantly accepted! :smile:

Quim10^-12