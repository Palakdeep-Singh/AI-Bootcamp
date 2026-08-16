import re
import pandas as pd


def preprocess(data):

    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]

    # extract dates
    dates = re.findall(pattern, data)

    # data frame banalo
    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})

    def parse_whatsapp_date(value):
        try:
            return pd.to_datetime(value, format='%d/%m/%Y, %H:%M - ', dayfirst=True, errors='coerce')
        
        except (TypeError, ValueError):
            return pd.to_datetime(value, dayfirst=True, errors='coerce')

    # parse different WhatsApp date formats safely (2-digit or 4-digit year)
    df['date'] = df['message_date'].apply(parse_whatsapp_date)
    df = df.dropna(subset=['date']).copy()

    # drop the raw string field after parsing
    df.drop(columns=['message_date'], inplace=True)

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

    # ignore blank messages and notification entries
    df = df[df['message'].fillna('').str.strip() != ''].copy()
    df = df[df['user'] != 'group_notification'].copy()

    # Now drop the original 'user_messages' column as it's no longer needed
    df.drop(columns=['user_messages'], inplace=True)

    # now also seperate the date time column.
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['date_only'] = df['date'].dt.date
    df['time'] = df['date'].dt.time
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df