import streamlit as st
import instaloader
import time
import pandas as pd
import requests
import os

# Initialize instaloader
loader = instaloader.Instaloader()

def get_instagram_data(account_name):
    try:
        profile = instaloader.Profile.from_username(loader.context, account_name)
    except Exception as e:
        st.write(f"Error fetching profile: {e}")
        return None

    data = []

    try:
        posts = profile.get_posts()
    except Exception as e:
        st.write(f"Error fetching posts: {e}")
        return None

    for post in posts:
        time.sleep(0.5)  # Increasing the delay to 5 seconds

        post_data = {
            'Date': post.date.strftime('%Y-%m-%d %H:%M:%S'),
            'Media': post.url,
            'Caption': post.caption,
            'Likes': post.likes, 
            'Comments': post.comments,
            'Type': '',
            'PostURL': f"https://www.instagram.com/p/{post.shortcode}"
        }
        
        if post.typename == 'GraphVideo':
            post_data['Type'] = 'video post'
        elif post.typename == 'GraphImage':
            post_data['Type'] = 'post'
        
        data.append(post_data)
        
    df = pd.DataFrame(data)
    return df

def main():
    st.title('Instagram Data Fetcher')

    accounts = st.text_area("Enter Instagram account names (comma-separated)").split(',')
    accounts = [account.strip() for account in accounts]

    if st.button('Submit'):
        if not accounts:
            st.write("Please enter Instagram account names.")
        else:
            for account_name in accounts:
                with st.expander(account_name):  # Each account will be a separate tab
                    df = get_instagram_data(account_name)

                    if df is not None:
                        for idx, row in df.iterrows():
                            st.markdown(f"### Date: {row['Date']}")
                            st.markdown(f'<iframe src="{row["PostURL"]}/embed" width="480" height="480" frameborder="0" scrolling="no" allowtransparency="true"></iframe>', unsafe_allow_html=True)

                            # Display the data as a table
                            st.table(pd.DataFrame({
                                'Caption': [row['Caption']],
                                'Likes': [row['Likes']],
                                'Comments': [row['Comments']],
                                'Type': [row['Type']]
                            }))

if __name__ == '__main__':
    main()
