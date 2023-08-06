from collective.flowplayer.browser.view import File


class FlowPlayerBlock(File):
    """Block view for flowplayer enabled files"""

    def href(self):
        """Fixes an issue where a logged in user with edit permission was not
        able to play the video due to a broken URL.

        This happened if the ID of the file-object (context) did not included
        the file-extension.
        """
        url = super(FlowPlayerBlock, self).href()
        parts = url.split('?')
        parts[0] = parts[0] + "/download"

        return '?'.join(parts)
