import frontmatter
from pathlib import Path, PosixPath
import sys

# 'path' == '_posts' in 'documentation'
# 'path' == 'build/html' in 'py-docs'
# 'path' == 'r' in 'r-docs'
try:
    path = str(sys.argv[1])
except:
    raise Exception("You need to specify a path that contains the files with front matter.")


def postsWithNoName(meta_to_check):
    failures = []
    for meta in meta_to_check:
        # Check #1 - do all non-redirect posts have names?
        if "name" not in meta and "redirect_to" not in meta:
            failures.append(post.metadata['permalink'])
    return failures

def postsWithTitle(meta_to_check):
    failures = []
    for meta in meta_to_check:
        # Check #2 - do any posts have titles?
        if "title" in meta:
            failures.append(post.metadata['permalink'])
    return failures

def duplicatePermalinks(meta_to_check):
    failures = []
    allPermalinks = []
    for meta in meta_to_check:
        # Check #3 - are there duplicate permalinks/redirect_froms?
        if "permalink" in meta and meta['permalink'] != '//plot.ly/products/dash/':
            if meta['permalink'] in allPermalinks:
                print(meta['permalink'])
                failures.append(meta['permalink'])
            else:
                allPermalinks.append(meta['permalink'])
        if "redirect_from" in meta:
            if meta['redirect_from'] in allPermalinks:
                failures.append(meta['redirect_from'])
            else:
                allPermalinks.append(meta['redirect_from'])
    return failures


def indexOverflow(meta_to_check):
    failures = []
    for meta in meta_to_check:
        # Check #4 - are there posts with order > 5 and 'page_type: example_index'?
        if "display_as" in meta and meta['display_as'] in categories:
            if "language" in meta and meta['language'] in languages:
                if "order" in meta and meta['order'] > 5:
                    if "page_type" in meta and meta['page_type'] == "example_index":
                        failures.append(meta['permalink'])
    return failures

def postsWithNoThumbnail(meta_to_check):
    failures = []
    for meta in meta_to_check:
        # Check #5 - does every post have a thumbnail?
        if "thumbnail" not in meta:
            if "display_as" in meta and meta['display_as'] in categories:
                if "language" in meta and meta['language'] in languages:
                    failures.append(meta['permalink'])
    return failures

def noTrailingSlash(meta_to_check):
    failures = []
    for meta in meta_to_check:
        # Check #6 - do any permalinks not end with a trailing slash?
        if "permalink" in meta:
            if meta['permalink'][-1] != "/":
                failures.append(meta['permalink'])
    return failures

checks = {
    "do all non-redirect posts have names?": postsWithNoName,
    "do any posts have titles?": postsWithTitle,
    "are there posts with order > 5 and 'page_type: example_index'?": indexOverflow,
    "are there duplicate permalinks/redirect_froms?": duplicatePermalinks,
    "does every post have a thumbnail?": postsWithNoThumbnail,
    "do any permalinks not end with a trailing slash?": noTrailingSlash,
}

categories = ["file_settings", "basic", "financial", "statistical", "scientific", "maps", "3d_charts", "multiple_axes"]
languages = ["python", "python/v3", "plotly_js", "r"]

paths = []
if path == "r":
    for suffix in ["Rmd"]:
        paths += [x for x in Path(path).glob("*."+suffix)]
else:
    # collect all paths
    for suffix in ["md", "html"]:
        paths += [x for x in Path(path).glob("**/*."+suffix)]

# collect all posts
meta_to_check = []
for path in paths:
    post = frontmatter.load(str(path))
    if len(post.metadata.keys()) > 0 and "jupyter" not in post.metadata:
        meta_to_check.append(post.metadata)



print("Begin CI Checks!\n")
passed = True
for message in checks:
    failures = checks[message](meta_to_check)
    print("***********************************!")
    print("Checking... {}".format(message))
    if len(failures) > 0:
        passed = False
        print("NOT PASSED!\n")
        print("List of failed permalinks:")
        print("**{}**".format(failures))
        print("\n")
    else:
        print("Passed!")
print("End CI Checks!\n")

if not passed:
    raise Exception("***********CI Checks Not Passed! Check Error Messages!*********************")
