from nicegui import APIRouter
import theme
from pages import (
    home_content, 
    get_structures_content,
    get_structure_content,
    get_forest_content,
    get_value_content
)

router = APIRouter()

@router.page('/')
def home_page():
    with theme.frame('Home'):
        home_content()

@router.page('/get-structures')
def get_structures_page():
    with theme.frame('Get structures'):
        get_structures_content()

@router.page('/get-structure')
def get_structure_page():
    with theme.frame('Get structure'):
        get_structure_content()

@router.page('/get-forest')
def get_forest_page():
    with theme.frame('Get forest'):
        get_forest_content()
    
@router.page('/get-value')
def get_value_page():
    with theme.frame('Get value'):
        get_value_content()