from .models import Message
from complaints.models import BlockList


def check_user_in_blocklist(sender, recipient):
    """
    Check if sender in recipient block list
    :param sender: User instance
    :param recipient: User instance
    :return: True if in block list
    """
    try:
        block_list = BlockList.objects.get(owner=recipient)
        if sender in block_list.users.all():
            return True
        else:
            return False
    except (BlockList.DoesNotExist, BlockList.MultipleObjectsReturned):
        return False


def send_message_helper(thread, text, sender):
    """
    Send message helper function
    :param thread: thread object
    :param text: message text
    :param sender: message sender (User object)
    :return: Message instance
    """
    message = Message()
    message.text = text
    message.thread = thread
    message.sender = sender
    message.save()
    return message