from nicegui import APIRouter
import theme
from pages import (
    home_content,
    rest_get_structures_content,
    rest_get_structure_content,
    rest_get_forest_content,
    rest_get_value_content
)

router = APIRouter()


@router.page('/')
def home_page():
    with theme.frame('Home'):
        home_content()


@router.page('/rest-get-structures')
def get_structures_page():
    with theme.frame('REST API - Get structures'):
        rest_get_structures_content()


@router.page('/rest-get-structure')
def get_structure_page():
    with theme.frame('REST API - Get structure'):
        rest_get_structure_content()


@router.page('/rest-get-forest')
def get_forest_page():
    with theme.frame('REST API - Get forest'):
        rest_get_forest_content()


@router.page('/rest-get-value')
def get_value_page():
    with theme.frame('REST API - Get value'):
        rest_get_value_content()
