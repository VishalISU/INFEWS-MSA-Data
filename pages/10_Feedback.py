import streamlit as st
from datetime import datetime



def save_comment(comment):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('comments.txt', 'a') as f:
        f.write(f'{timestamp}: {comment}\n')

def main():
    st.title(':speech_balloon: Feedback Form')

    # Text input field for the comment
    '''
    What more would you like to see cosimulated? 
    What can be improved? 
    '''
    comment = st.text_input('Enter your comments below')

    # Submit button
    if st.button('Submit'):
        if comment:
            save_comment(comment)
            st.success('Thank you for your feedback!')
            st.text('Your comment has been saved.')
        else:
            st.warning('Please enter a comment.')

if __name__ == '__main__':
    main()

