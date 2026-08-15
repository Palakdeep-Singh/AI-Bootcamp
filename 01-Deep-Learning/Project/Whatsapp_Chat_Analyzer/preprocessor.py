import re
import pandas as pd


def preprocess(data):

    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]

    # extract dates
    dates = re.findall(pattern, data)

    # data frame banalo
    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})
    # message ki date and time seperate krdo
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%Y, %H:%M - ")

    # now rename krdo
    df.rename(columns={"message_date": "date"}, inplace=True)

    extracted_users = []
    extracted_messages = []

    for msg_content in df['user_messages']:
        # This pattern captures the sender (non-greedy) up to the first colon and space,
        # and the rest as the message. If no colon is found, it's a group notification.
        match = re.match(r'([^:]+?):\s(.*)', msg_content)
        if match:
            # If a colon and space are found, it's a message from a user
            extracted_users.append(match.group(1).strip())
            extracted_messages.append(match.group(2).strip())
        else:
            # Otherwise, it's likely a group notification or a message without a clear sender
            extracted_users.append("group_notification")
            extracted_messages.append(msg_content.strip())  # Keep the full content as message

    df['user'] = extracted_users
    df['message'] = extracted_messages

    # Now drop the original 'user_messages' column as it's no longer needed
    df.drop(columns=['user_messages'], inplace=True)

    # now also seperate the date time column.
    df['year'] = df['date'].dt.year
    df["month"] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day

    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    df.drop(columns=['date'], inplace=True)
    
    return df