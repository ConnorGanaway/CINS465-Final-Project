# Next thing to work on in project:

1. Make posts only appear for the community they are tied too
  - I need to find the list rendering function in vue.js, so it pulls
    from the cur_community json page.
  - How do I edit it so it uses a link with a <std:community_id> which
    changes in the link

2. Declutter Menu
  - Remove "Reddit Clone, Logout, and Admin" links
  - Add dropdown(just like right side) for communities
  - Add logout link (moved from right left side) to the dropdown for profile
  - Repurpose footer box:
    - Fix size issue (this will most likely go away when I don't render communities there)
    - Create funny schmeddit logo for the website to be out on the footer
    - Add my name, year, class, and social links (With nice looking pictures)

3. Followed communities feature
  - add users who followed to the community model
  - on the index page, if the user is on the community models followed list attribute.
    render the community in the list

4. Up Vote And Down vote feature (Stretch Goal)
  - Find images without transparent background
  - Resize Images Correctly (Or find smaller images)
  - Add javascript code to change the vote number on the website
    - Increment when the upvote image is clicked
    - Decrement when the downvote image is clicked
    - Also update the vote attribute for the suggestion model in the database
