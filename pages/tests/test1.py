from streamlit.testing.v1 import AppTest

# def test_smoke():
#     test = AppTest("../../app.py", default_timeout = 10).run()
#     assert not test.exception

# def test_home():
#     test = AppTest("../../app.py", default_timeout = 10).run()
#     home = test.switch_page("pages/home.py").run()
#     assert not home.exception

# def test_homw_login():
    # test = AppTest("../../app.py", default_timeout = 10).run()
home = AppTest("../home.py", default_timeout = 10).run()
text = home.markdown.values
# assert text == "Hello"
print(home)
