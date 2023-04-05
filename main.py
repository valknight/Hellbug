import os
import tumblr
import cohost.models.user
from cohost.models.project import EditableProject
from cohost.models.block import MarkdownBlock
import sys

def getCohostProject() -> EditableProject:
    cohostEmail = os.environ.get('COHOST_EMAIL')
    if cohostEmail == None:
        raise EnvironmentError('COHOST_EMAIL needs to be defined')
    cohostPass = os.environ.get('COHOST_PASS')
    if cohostPass == None:
        raise EnvironmentError('COHOST_PASS needs to be defined')
    # Get the session
    cohostSession = cohost.models.user.User.login(cohostEmail, cohostPass)
    print('logged into Cohost - getting project')

    cohostProject = os.environ.get('COHOST_PROJECT')
    # Get the cohost project
    if cohostProject == None:
        cohostProject = cohostSession.defaultProject
        print('COHOST_PROJECT undefined - defaulting to {}'.format(cohostProject.handle))
    else:
        cohostProject = cohostSession.getProject(cohostProject)
        if type(cohostProject) != EditableProject:
            raise EnvironmentError('change COHOST_PROJECT - you do not have edit permission for {} on cohost.org!'.format(os.environ.get('COHOST_PROJECT')))
    print('got project {} ({})'.format(cohostProject.handle, cohostProject.displayName))
    return cohostProject

tumblrUrl = os.environ.get('TUMBLR_URL')
if tumblrUrl == None:
    raise EnvironmentError('TUMBLR_URL needs to be defined (eg, "yourusername.tumblr.com")')

def makeDirIfNotExists(path: str):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def setupDirectories():
    makeDirIfNotExists('data')
    makeDirIfNotExists('data/blogs')

def main():
    setupDirectories()
    blog = tumblr.TumblrBlog(tumblrUrl)
    # Ok, got to this point, blog must exist!
    blogDir = 'data/blogs/{}'.format(blog.uuid.replace(':', '-'))
    makeDirIfNotExists(blogDir)
    latestPostId = blog.latestPostId
    lastPostId = "0"
    try:
        with open('{}/lastPostId'.format(blogDir), 'r') as f:
            lastPostId = f.read()
    except FileNotFoundError:
        pass
    if lastPostId >= latestPostId:
        print('latest post synced')
        sys.exit(0)
    print('new post with ID {}!'.format(latestPostId))
    print('logging into cohost...')
    cohostProject = getCohostProject()
    print(blog.latestPost['tags'])
    postBlocks = [MarkdownBlock(blog.latestPostWithCohostStyling))]
    tags = blog.latestPost['tags']
    tags.append('hellbug')
    tags.append('bot')
    tags.append('cohost.py')
    post = cohostProject.post(blog.latestPost['summary'], postBlocks, tags=tags)
    if post is None:
        print('posted to cohost, but, not able to access (could be a draft!)')
    else:
        print('posted to cohost at {}'.format(post.url))
    with open('{}/lastPostId'.format(blogDir), 'w') as f:
        f.write(str(latestPostId))

if __name__ == '__main__':
    main()