import json
import os
import pytumblr

tumblrTag = os.environ.get("TUMBLR_TAG")
if (tumblrTag == None):
    tumblrTag = "txt"
    print("defaulting tumblrTag to txt")

tumblrKey = os.environ.get("TUMBLR_KEY")
if (tumblrKey == None):
    raise EnvironmentError("TUMBLR_KEY is not defined")


client = pytumblr.TumblrRestClient(tumblrKey)


class TumblrBlog:
    def __init__(self, tumblrUrl):
        self.tumblrUrl = tumblrUrl
        self.refresh()
    
    def refresh(self):
        if (tumblrTag != ""):
            self.profile = client.posts(self.tumblrUrl, type="text", tag=tumblrTag)
        else:
            self.profile = client.posts(self.tumblrUrl, type="text")
        if self.profile.get("meta", {}).get("status") == 404:
            raise AttributeError("\"{}\" is not a valid tumblr URL - make sure you didn't include https://".format(self.tumblrUrl))

    @property
    def posts(self):
        return self.profile.get("posts")
    
    @property
    def latestPost(self):
        p = self.posts
        if len(p) == 0:
            return None
        return p[0]
    
    @property
    def latestPostId(self):
        if self.latestPost == None:
            return "-1"
        return self.latestPost["id_string"]
    
    
    @property
    def latestPostAsHTML(self):
        post = self.latestPost
        if post == None:
            return ""
        return post["body"].replace("\n", "") # Cohost"s styling will handle line breaks for us, we"re good.
    
    @property
    def latestPostWithCohostStyling(self):
        latestPost = self.latestPostAsHTML
        if latestPost == "":
            return latestPost
        latestPost = latestPost.replace('<p>', '<p style="color:white;">')
        latestPost = '<div style="padding:5px;background-color:#34526f;border-radius:5px;">{}</div>'.format(latestPost)
        latestPost += '<small style="color: rgba(1,1,1,0.5);"><a href=\"https://github.com/valknight/Hellbug\">Hellbug</a> - made with <a href=\"https://github.com/valknight/cohost.py\">cohost.py</a></small>'
        return latestPost
    
    @property
    def uuid(self):
        return self.profile.get("blog", {}).get("uuid")


if __name__ == "__main__":
    blog = TumblrBlog("vallerie-cohost")
    print(blog.latestPostWithCohostStyling)