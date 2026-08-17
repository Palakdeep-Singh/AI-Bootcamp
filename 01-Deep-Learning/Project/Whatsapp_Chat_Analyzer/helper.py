from urlextract import URLExtract

extract = URLExtract()


def fetch_stats(selected_user,df):
  
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]
  
  num_messages = df.shape[0]
  words = []
  
  links = []
  
  for msgs in df['message']:
    words.extend(msgs.split())
    links.extend(extract.find_urls(msgs))
    
  # Count messages that are exactly 'Media omitted'
  media_count = df[df['message'] == '<Media omitted>'].shape[0]
  

  return num_messages,len(words),media_count,len(links)