import wx
import sqlite3
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import asyncio
import aiohttp
import os
import logging
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("OCTOPART_API_KEY")
logging.basicConfig(filename='circuit_simulator.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s')

Base = declarative_base()

class Diagram(Base):
    __tablename__ = 'diagrams'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    data = Column(String)

class Component(Base):
    __tablename__ = 'components'
    id = Column(Integer, primary_key=True)
    component_id = Column(String)
    data = Column(String)

engine = create_engine('sqlite:///circuit_diagrams.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class OctopartAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    async def fetch_component_info(self, component_id):
        url = f"https://octopart.com/api/v4/rest/products/{component_id}"
        params = {"apikey": self.api_key}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logging.warning(f"API request failed with status: {response.status}")
                        return None
            except Exception as e:
                logging.error(f"Failed to fetch component info: {e}")
                return None

class CircuitDatabase:
    def __init__(self, db_name="circuit_diagrams.db"):
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS diagrams
                         (id INTEGER PRIMARY KEY, name TEXT, data TEXT)''')
            c.execute('''CREATE TABLE IF NOT EXISTS components
                         (id INTEGER PRIMARY KEY, component_id TEXT, data TEXT)''')
            conn.commit()

    def save_diagram(self, name, data):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO diagrams (name, data) VALUES (?, ?)', (name, data))
            conn.commit()

    def load_diagram(self, name):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('SELECT data FROM diagrams WHERE name=?', (name,))
            row = c.fetchone()
        return row[0] if row else None

    def save_component(self, component_id, data):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO components (component_id, data) VALUES (?, ?)', (component_id, data))
            conn.commit()

    def load_component(self, component_id):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('SELECT data FROM components WHERE component_id=?', (component_id,))
            row = c.fetchone()
        return json.loads(row[0]) if row else None

class CircuitDesigner:
    def __init__(self, db, octopart_api):
        self.db = db
        self.octopart_api = octopart_api

    def design_circuit(self, parameters):
        components = parameters.get('components', [])
        design = {'components': components, 'connections': []}
        for i in range(len(components) - 1):
            design['connections'].append((components[i], components[i + 1]))
        return design

    def render_circuit(self, design):
        fig, ax = plt.subplots()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

        for idx, component in enumerate(design['components']):
            x, y = np.random.rand(2) * 8 + 1
            ax.text(x + 0.5, y + 1.2, component, ha='center')
            ax.plot([x, x + 1], [y, y], 'k-')

        for connection in design['connections']:
            start_idx = design['components'].index(connection[0])
            end_idx = design['components'].index(connection[1])
            start_x, start_y = np.random.rand(2) * 8 + 1.5
            end_x, end_y = np.random.rand(2) * 8 + 1.5
            ax.plot([start_x, end_x], [start_y, end_y], 'k-')

        return fig

    async def fetch_and_store_component(self, component_id):
        try:
            component_data = await self.octopart_api.fetch_component_info(component_id)
            if component_data:
                self.db.save_component(component_id, json.dumps(component_data))
                return component_data
            else:
                logging.warning(f"No data received for component: {component_id}")
                return None
        except Exception as e:
            logging.error(f"Error fetching and storing component: {str(e)}")
            return None

class MainFrame(wx.Frame):
    def __init__(self, parent, title, db, octopart_api):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))
        self.db = db
        self.circuit_designer = CircuitDesigner(db, octopart_api)
        self.initUI()

    def initUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(panel, -1, self.figure)
        vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

        btnPanel = wx.Panel(panel)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        saveButton = wx.Button(btnPanel, label='Save', size=(70, 30))
        loadButton = wx.Button(btnPanel, label='Load', size=(70, 30))
        hbox.Add(saveButton)
        hbox.Add(loadButton, flag=wx.LEFT, border=5)
        btnPanel.SetSizer(hbox)

        vbox.Add(btnPanel, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        saveButton.Bind(wx.EVT_BUTTON, self.onSave)
        loadButton.Bind(wx.EVT_BUTTON, self.onLoad)

        panel.SetSizer(vbox)
        self.SetSize((800, 600))
        self.Centre()

    def onSave(self, event):
        diagram_data = {"example": "data"}
        json_data = json.dumps(diagram_data)
        self.db.save_diagram("Example Circuit", json_data)
        wx.MessageBox('Diagram saved', 'Info', wx.OK | wx.ICON_INFORMATION)

    def onLoad(self, event):
        json_data = self.db.load_diagram("Example Circuit")
        if json_data:
            diagram_data = json.loads(json_data)
            # Implement rendering logic based on `diagram_data`
            wx.MessageBox('Diagram loaded', 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('No diagram found', 'Error', wx.OK | wx.ICON_ERROR)

def main():
    if not API_KEY:
        logging.error("No Octopart API key provided. Please set the 'OCTOPART_API_KEY' environment variable.")
        return

    db = CircuitDatabase()
    octopart_api = OctopartAPI(API_KEY)
    
    app = wx.App()
    ex = MainFrame(None, title='Circuit Simulator', db=db, octopart_api=octopart_api)
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()