from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

## .\uvicorn_start.bat
## .\uvicorn_stop.bat

app = FastAPI()

# 👇 Only allow your Vue app's Railway domain
origins = [
    "https://webmonitorv002-production.up.railway.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # your frontend domain
    allow_credentials=True,
    allow_methods=["*"],     # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # allow all headers
)

## **************************************************************************

DATABASE_URL = "postgresql://postgres:oAsNnJNByWEiKBJUpJYyKGNxlparYhxv@crossover.proxy.rlwy.net:11328/railway"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# this comment contain the database tables:
"""
first table:signal_list
columns: signal_list_id, signal_list_name, timeframe, trigger_usability

second table:signals
columns: signal_list_id, indicator, indicator_order_to_be_significant, signalname, active
"""


class Item(BaseModel):
    name: str
    description: str = None

class signal(BaseModel):    
    signal_list_name: str
    timeframe: str
    trigger_usability: str
    signalname: str
    is_signal_active: str



@app.post("/items/")
async def create_item(inParams: signal):
    try:
        
        # Example SELECT query
        #---------------------- OPEN DATABASE ---------------
        db = SessionLocal()
        #----------------------------------------------------

        ##**************************************************************************
        ##                            READ SIGNAL ID
        ##**************************************************************************

        """ api input parameters:
                signal_list_name: str
                timeframe: str
                trigger_usability: str
                signalname: str
                command: str
        """

        sql_text = """ SELECT tbl_s.signal_id 
                  FROM signals as tbl_s
                  inner join signal_list as tbl_sl ON tbl_sl.signal_list_id = tbl_s.signal_list_id
                  WHERE tbl_sl.signal_list_name = :signal_list_name
                  AND tbl_sl.timeframe = :timeframe
                  AND tbl_sl.trigger_usability = :trigger_usability
                  AND tbl_s.signalname = :signalname
                """
        #sql_text = """ SELECT h.signal_list_name, h.trigger_usability,h.timeframe,
        #                d.indic_order_significant as priority, d.signalname, d.active
        #            FROM public.signal_list h
        #            inner join public.signals d on d.signal_list_id = h.signal_list_id 
        #            where d.active =  1
        #            and h.signal_list_name = :signal_list_name
        #            order by h.signal_list_name, h.trigger_usability,h.timeframe_order, d.indic_order_significant
        #        """
        
        sql_text = sql_text.replace("\n"," ")
        result = db.execute( text(sql_text),
            {"signal_list_name": inParams.signal_list_name
             , "timeframe": inParams.timeframe
             , "trigger_usability": inParams.trigger_usability
             , "signalname": inParams.signalname
            }
        )
        row = result.fetchone()
        
        
        ##**************************************************************************
        ##                            READ COMMAND
        ##**************************************************************************

        is_signal_active = -1
        if inParams.is_signal_active == '1':
            is_signal_active = 1
        elif inParams.is_signal_active == '0':
            is_signal_active = 0
        if is_signal_active == -1:
            raise Exception("Invalid is_signal_active value")
        
        
        ##***************************************************************************
        ##                            UPDATE SIGNAL
        ##**************************************************************************

        update_query = text("""
            UPDATE signals
            SET active = :is_signal_active
            WHERE signal_id = :signal_id
        """)
        update_params = {
            "is_signal_active": is_signal_active,
            "signal_id": row.signal_id,
        }
        db.execute(update_query, update_params)
        
        ##***************************************************************************
        ##                            COMMIT CHANGES
        ##**************************************************************************
        db.commit()

        ## Return the updated row ID or any other relevant information
        return {
            "resultx": "OK",
            "errorx": "NA",
            "inParams": inParams,
        }
    except SQLAlchemyError as e:
        print("Database Error:", e)
        return {"result":"NG",
                "error": str(e)}
    except Exception as e:
        print("Error:", e)
        return {"result":"NG",
                "error": str(e)}
    finally:
        if 'db' in locals():
            db.close()
    
    


@app.post("/getAll/")
async def consultAll(inParams: signal):
    try:
        
        # Example SELECT query
        #---------------------- OPEN DATABASE ---------------
        db = SessionLocal()
        #----------------------------------------------------

        ##**************************************************************************
        ##                            READ SIGNAL ID
        ##**************************************************************************

        """ api input parameters:
                signal_list_name: str
                timeframe: str
                trigger_usability: str
                signalname: str
                command: str
        """


        sql_text = """ SELECT h.signal_list_name, h.trigger_usability,h.timeframe,
                        d.indic_order_significant as priority, d.signalname, d.active
                    FROM public.signal_list h
                    inner join public.signals d on d.signal_list_id = h.signal_list_id 
                    where d.active =  1
                    and h.signal_list_name = :signal_list_name
                    order by h.signal_list_name, h.trigger_usability,h.timeframe_order, d.indic_order_significant
                """
        
        sql_text = sql_text.replace("\n"," ")
        result = db.execute( text(sql_text),
            {"signal_list_name": inParams.signal_list_name
             , "timeframe": inParams.timeframe
             , "trigger_usability": inParams.trigger_usability
             , "signalname": inParams.signalname
            }
        )
        dataFrame_result = pd.DataFrame(result.fetchall(), columns=result.keys())
      
        
        ##***************************************************************************
        ##                            COMMIT CHANGES
        ##**************************************************************************
        db.commit()

        ## Return the updated row ID or any other relevant information
        return {
            "result": "OK",
            "error": "NA",
            "inParams": dataFrame_result.to_dict(orient='records'),
        }
    except SQLAlchemyError as e:
        print("Database Error:", e)
        return {"result":"NG",
                "error": str(e)}
    except Exception as e:
        print("Error:", e)
        return {"result":"NG",
                "error": str(e)}
    finally:
        if 'db' in locals():
            db.close()
    
    


    '''
    ## Insert a new row into signal_list
        #insert_query = text("""
        #    INSERT INTO signal_list (signal_list_name, timeframe, trigger_usability)
        #    VALUES (:name, :timeframe, :trigger_usability)
        #    RETURNING signal_list_id
        #""")
        ## Example values for timeframe and trigger_usability
        #params = {
        #    "name": item.name,
        #    "timeframe": "1h",
        #    "trigger_usability": True
        #}
        #insert_result = db.execute(insert_query, params)
        #db.commit()
        #inserted_id = insert_result.fetchone()[0]
        #print("Inserted signal_list_id:", inserted_id)

    '''




    ##**************************** Railway Config ******************************
    ## Railway start command:
    ## uvicorn main:app --host 0.0.0.0 --port $PORT
    ##
    ##
    ## Railway how to call the API:
    ## https://fastapi-app-production-d82b.up.railway.app/items/
    ##
    ## Example of input parameters:
    ##**************************************************************************
    ##  {
    ##  "signal_list_name": "eth_usd",
    ##  "timeframe": "5m",
    ##  "trigger_usability": "buy",
    ##  "signalname": "ema9<=ema55",
    ##  "command": "ema9>ema55"
    ##  }
    ##
    ## 


    ##**************************************************************************