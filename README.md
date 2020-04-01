# star_wars

To improve my knowledge of network graphs and practice app building, I built an interactive 3D network diagram showing which star wars characters shared a screen together.

# Data Collection

Using a combination of wookiepedia and https://www.abc.net.au/news/2015-12-16/star-wars-every-scene/7013826 I built a csv file of each scene from each film showing which characters were present. 

# Networking

I used a combination of pandas and networkx to build the network for each film and then attached them together. However, this created a super messy diagram with 11 films of characters meshed together on a 2D plane. I wanted my app to be easy to read and informative, so I decided to make an interactive 3D network plot. 

# Going 3D

Using plotly's instructions https://plotly.com/python/v3/3d-network-graph/, I created a go.Figure object which took all the nodes in 3D space and plotted them, I then also attached the edges in a similar way. I colour coded each node by which film the character first appeared in and created hover info which told you how many other characters a given person shared a scene with in the network (the app allows you to view connections across as many films as you would like).

To finish off the app, I added in a function which allows a user to click on a node and underneath give a list of characters that person appeared with.
