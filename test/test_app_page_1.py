from streamlit.testing.v1 import AppTest

def test():
    # Test that the app starts up.
    at=AppTest.from_file("pages/1_Reclutamiento y Seleccion en el Estado.py").run()
    assert not at.exception
    
