from dataclasses import dataclass


@dataclass
class Languages:
    english = 'en'
    german = 'ge'


@dataclass
class Variables:
    padding = 15

    language: Languages = Languages.german


class Translation:
    def __init__(self, english: str = None, german: str = None):
        self._english = english
        self._german = german

    @property
    def text(self) -> str:
        name = None
        match Variables.language:
            case Languages.english:
                name = self._english
            case Languages.german:
                name = self._german
        if name is None:
            return self._english
        else:
            return name


@dataclass
class TextTranslation:
    boundary_conditions = Translation('boundary conditions', 'Randbedingungen')
    cancel = Translation(english='cancel', german='Abbrechen')
    corner = Translation(english='corner, grad =', german='Winkel, grad = ')
    profile_with_parameters = Translation(english='profile \nwith \nparameters', german='Profile \nmit \nParameters')
    points_import_Excel: Translation = Translation(english='Excel import')
    points_export_Excel: Translation = Translation(english='Excel export')
    comments: Translation = Translation(english='comments', german='Kommentare')
    plus_one_point = Translation(english='+ one point', german='+ einen Punkt')
    delete_the_point = Translation(english='delete the point', german='den Punkt entfernen')
    open_file = Translation(english='Open', german='Offnen')
    save_file = Translation(english='Save', german='Speichern')
    save_file_as = Translation(english='Save as', german='Speichern wie')
    back = Translation(english='Back', german='Zurück')
    forward = Translation(english='Forward', german='Vorwärts')
    points = Translation(english='Points', german='Punkte')
    rolled_section = Translation(english='rolled section', german='gewalzte Profile')
    span = Translation('span, m', 'Feldlänge, m')
    i_sections = Translation(english='I sections', german='I Profile')
    u_sections = Translation(english='U sections', german='U Profile')
    l_sections = Translation(english='L sections', german='Winkel')
    o_sections = Translation(english='O sections', german='Hohlprofile')
    isosceles = Translation(english='isosceles', german='gleichschenklig')
    not_isosceles = Translation(english='not isosceles', german='ungleichschenklig')
    circular = Translation(english='circular', german='kreisförmig')
    square = Translation(english='square', german='quadratisch')
    rectangular = Translation(english='rectangular', german='rechteckig ')
    lines = Translation(english='Lines', german='Linien')
    section = Translation(english='Section', german='Querschnitten')
    concrete = Translation(english='concrete', german='Beton')
    steel = Translation(english='steel', german='Stahl')
    welded_profile = Translation(english='welded profile', german='geschweißte Profile')
    wood = Translation(english='wood', german='Holz')

