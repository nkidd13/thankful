from App import App

thankfulApp = App()
thankfulApp.run()



# if state.loggedIn:
#     st.write("# Welcome ", state.fName, " we're glad you're here.")
#     st.write("Thanksgiving is the season to reflect before the beginning of the new year. "
#              "Let your mind pleasantly wonder over the good memories, moments you laughed hard, tried new things, "
#              " explored new places, and spent quality time with friends and family. \n\nEven if times were not always good, "
#              "remember you have perservered and made it to the place you are today. In the face of grief or hardship "
#              "there are always small lessons and blessings to be thankful for. \n\nTo end this thoughtful journey reflect "
#              "on the things you love most, who or what inspired you, and what your future goals may be.  \n\n\n"
#              "Finally, sit down as a family and think of a couple things you are all grateful for this season. :)")
#     st.sidebar.markdown("Enter your responses here")
#
#     userList = st.sidebar.text_input("Enter items as a comma separated list or one at a time")
#     thanks = st.sidebar.button("Give thanks")
#     if thanks and len(userList) > 0:
#         temp = addToThanksList(userList, state)
#
#     displayFamily(state)
#
#     st.subheader("Feel free to share your family log in information with extended family."
#                  " You will be able to see a mixture of what people are thankful for.")
#
#     # refresh user token if needed
#     if state.user != None and state.user["expiresIn"] == 0:
#         state.user = auth.refresh(state.user['refreshToken'])
#
# else:
#     st.sidebar.markdown("""
#     # Log in with your family to keep track of what everyone is thankful for!
#     New here? come up with a fun and unique family name. If you already have one, welcome back!
#
#     Feel free to share these log in details with your extended family so they can join the fun.
#      Come back after Thanksgiving to see what everyone entered.
#      """)
#     familyName = st.sidebar.text_input("What is your family name?")
#     email = st.sidebar.text_input("Enter new or pre-registered email")
#     newFam = st.sidebar.button("New Fam Enter Here")
#     oldFam = st.sidebar.button("Existing Fam Enter Here")
#
#     if newFam and len(familyName) > 0 and len(email) > 0 :
#         user = createNewFamily(familyName, email, auth, state.db)
#         state.user = user
#         state.fName =  familyName
#         state.loggedIn = True
#
#     elif oldFam and len(familyName) > 0 and len(email) > 0 :
#         user = signInFamily(familyName, email, auth, db)
#         state.user = user
#         state.fName =  familyName
#         state.loggedIn = True
#     else:
#         state.loggedIn = False
#
#     #display a wordcloud of all family data.
#     st.title("Thanksgiving Reflections")
#     st.write("Join to keep track of what you are thankful for this year!")
#     familyCount = countFamilies(state)
#     st.write("So far ", countFamilies(state), " families have joined.\n\n ")
#     if familyCount > 0:
#         st.write("_Here is a sneak peak of what everyone is thankful for._")
#
#         #display word cloud
#         displayAllFamilies(state)
#     else:
#         st.write("You could be the first to join. ")