# Import python packages
import requests
smoothiefroot_response = requests.get('https://my.smoothiefroot.com/api/fruit/watermelon")
                                      st.text(smoothiefroot_response.json())
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"customized smoothies ")
st.write(
  """
  Choose the fruits you want in your custom Smoothie! 
  """
)

# option = st.selectbox(
#     "what is your favourite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("You selected:", option)

# title = st.text_input("Name on smoothie")
name_on_order = st.text_input("Name on order")
# st.write("The name on your smoothie will be :", title)
st.write("The name on your smoothie will be :", name_on_order)



# title = st.text_input('Movie title', 'Life of Brian')
# st.write('The current movie title is', title)

cnx = st.connection("snowflake")
session=cnx.session()

my_dataframe= session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# st.dataframe(data=my_dataframe,use_container_width=True)

ingredients_list=st.multiselect(
    'choose upto 5 ingredients:'
    , my_dataframe
    ,max_selections=5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen + ' '

    # st.write(ingredients_string)


    my_insert_stmt="""insert into smoothies.public.orders(ingredients,name_on_order)
                    values('"""+ ingredients_string + """','"""+ name_on_order +"""')"""

    # st.write(my_insert_stmt)
    time_to_insert=st.button('Submit order')

    if time_to_insert:
    # if ingredients_string:
        session.sql(my_insert_stmt).collect()

        st.success('your smoothie is ordered ',icon="✅")
        st.success('Your Smoothie is ordered, ' + name_on_order + '!')
