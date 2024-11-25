from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

# Connection to my database
connection = create_engine("mysql+mysqlconnector://natynic@2024:Sql-2024@localhost/servdatabase", echo=True)
Session = sessionmaker(bind=connection)
Base = declarative_base()

# My table specification from database
class Evenimente(Base):
    __tablename__ = "evenimentecrestine"
    id = Column(Integer, primary_key=True)
    tema = Column("tema", String(50))
    invitati = Column("invitati", String(50))
    locatie = Column("locatie", String(50))
    data = Column("data", String(50))
    ora = Column("ora", String(50))

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        
        session = Session()
        events = session.query(Evenimente).all()
        events_list = [self.serialize_event(event) for event in events]
        session.close()

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(events_list).encode('utf-8'))
        
    def do_POST(self):
       
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        event_data = json.loads(post_data)

        session = Session()
        new_event = Evenimente(
                tema=event_data['tema'],
                invitati=event_data['invitati'],
                locatie=event_data['locatie'],
                data=event_data['data'],
                ora=event_data['ora']
            )
        session.add(new_event)
        session.commit()

        serialized_event = self.serialize_event(new_event)
        session.close()

        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(serialized_event).encode('utf-8'))
       
    def do_PUT(self):

        content_length = int(self.headers["Content-length"])
        put_data = self.rfile.read(content_length)
        event_data = json.loads(put_data)

        session = Session()
        event = session.query(Evenimente).filter_by(id = event_data["id"]).first()

        if event:
            event.tema = event_data.get("tema", event.tema)
            event.invitati =  event_data.get("invitati", event.invitati)
            event.locatie = event_data.get("locatie", event.locatie)
            event.data = event_data.get("data", event.data)
            event.ora = event_data.get("orea", event.ora)
            session.commit()

            serialized_event = self.serialize_event(event)
            session.close()

            self.send_response(200)
            self.send_header( "Content-type", "application/json")     
            self.end_headers()   
            self.wfile.write(json.dumps(serialized_event).encode('utf-8'))
         

    def do_DELETE(self):
        content_length = int(self.headers ["Content-length"])
        delete_data = self.rfile.read(content_length)
        event_data = json.loads(delete_data)

        session = Session()
        event = session.query(Evenimente).filter_by(id = event_data["id"]).first()

        if event:
            session.delete(event)
            session.commit()
            session.close()

        self.send_response(200)
        self.send_header( "Content-type", "application/json")     
        self.end_headers()   
        self.wfile.write(json.dumps({'message': 'Event deleted successfully'}).encode('utf-8'))
        
    def serialize_event(self, event):    # convert data from the database in JSON mode for response / because we retrive data using SQLAlchemy's ORM (Object-Relational Mapping).
        return {
            'id': event.id,
            'tema': event.tema,
            'invitati': event.invitati,
            'locatie': event.locatie,
            'data': event.data,
            'ora': event.ora
        }

def main():
    PORT = 8020
    server = HTTPServer(('', PORT), RequestHandler)
    print("Naty server running on port %s " % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()

        
