import requests
import logging


log = logging.getLogger(__name__)


class Pinterest:
    """
    Class, that implements simple API to post to pin
    """
    create_board_url = "https://api.pinterest.com/v1/boards/?access_token={token}&fields=id%2Cname%2Curl"
    pins_url = "https://api.pinterest.com/v1/pins/?access_token={token}&fields=id%2Clink%2Cnote%2Curl"
    get_user_board_url = "https://api.pinterest.com/v1/me/boards/?access_token={token}&fields=id%2Cname%2Curl"

    def __init__(self, access_token, user):
        """
        Create instance. Init access_token, board_name, board_id
        :param access_token: str user's access token to pinterest
        :param user: <User> User object
        """
        self.access_token = access_token
        api_url = self.create_board_url.format(token=self.access_token)
        self.board_name = user.username + str(user.pk)
        # Try to create board 'username<pk>'
        response = requests.post(api_url, json={"name": self.board_name})
        data = response.json().get('data', None)
        if data:
            self.board_id = data.get('id')
        else:
            # If can't create board search it in created earlier
            api_url = self.get_user_board_url.format(token=self.access_token)
            response = requests.get(api_url)
            data = response.json().get('data', None)
            if data:
                for board in data:
                    if board['name'] == self.board_name:
                        self.board_id = board['id']
                    else:
                        log.error("No board found")
            else:
                log.error("Incorrect response")

    def post_message(self, message, image_url):
        """
        Try to create pin.
        :param message: str Pin message
        :param image_url: str image url to pin
        :return: None
        """
        if self.board_id:
            api_url = self.pins_url.format(token=self.access_token)
            request_data = {"board": self.board_id, "note": message, "image_url": image_url}
            response = requests.post(api_url, json=request_data)
            log.debug(response.json())
        else:
            log.debug("No board id. Can't add pin")

