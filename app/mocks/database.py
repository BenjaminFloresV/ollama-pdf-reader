

mock_database = [
    {
        "id": 1,
        "competencia_id": 5,
        "competencia_name": "Penal",
        "rit": "Ordinaria-6067-2025",
        "tribunal": "2º Juzgado de Garantia de Santiago",
        "ruc": "2500736148-6",
        "caratulado": "LEONARDO MAURICIO CAMPOS RODRIGUEZ C/ CRISTIAN ALFONSO BARRIOS ARAVENA",
        "fecha_ingreso": "01/07/2025",
        "estado_causa": "Tramitacion.",
        "tipo_consulta": "normal",
        "main_task_id": "9669e8bd-0465-41ed-9f95-6e95f289208f",
        "main_task_started": "05/08/2025 03:13:29",
        "start_date": "01/07/2025",
        "end_date": "02/07/2025",
        "tribunal_id": 1221,
        "detail": {
            "is_reserved": False,
            "litigantes": [
            {
                "tipo": "Denunciado.",
                "nombre": "CRISTIAN ALFONSO BARRIOS ARAVENA",
                "situacion_libertad": "Libre."
            },
            {
                "tipo": "Denunciante.",
                "nombre": "LEONARDO MAURICIO CAMPOS RODRIGUEZ",
                "situacion_libertad": ""
            },
            {
                "tipo": "Fiscal.",
                "nombre": "FISCAL GENERICO TRIBUNAL 1221",
                "situacion_libertad": ""
            },
            {
                "tipo": "Victima.",
                "nombre": "CONFIDENCIAL",
                "situacion_libertad": ""
            },
            {
                "tipo": "Testigo.",
                "nombre": "LEONARDO MAURICIO CAMPOS RODRIGUEZ",
                "situacion_libertad": ""
            }
            ],
            "associated_pdfs": [
            {
                "s3_url": "https://poder-judicial-test.s3.us-east-1.amazonaws.com/pdf/fb374926-725e-4b63-b68c-2a677e9ca8ca.pdf",
                "method": "get",
                "action": "https://oficinajudicialvirtual.pjud.cl/ADIR_871/penal/documentos/newebookpenal.php",
                "hidden_input_name": "dtaEbook",
                "hidden_input_value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvb2ZpY2luYWp1ZGljaWFsdmlydHVhbC5wanVkLmNsIiwiYXVkIjoiaHR0cHM6XC9cL29maWNpbmFqdWRpY2lhbHZpcnR1YWwucGp1ZC5jbCIsImlhdCI6MTc1NDM2Mzc3MSwiZXhwIjoxNzU0MzY3MzcxLCJkYXRhIjoieExxNlZvWStnbXJhQlZGS0Y5VzkwaVloblNjQWZoR2lsSFZRcVY2eGVnbmduZUg5MU9NNWhCbTc0NGdxSlkyVHlhVmJrMlkxQ2J4OG0zTlZIbWQrUlFUYit3cXM0WFwvcURZMU5tdEd3eFlBc1FHU3JudG9GS3p4MlQ5V1J4RXlzIn0.CMxuDHaXcgxUUoBFeHsb-od6YxwxwzGWSShsamiALNc"
            },
            {
                "s3_url": "https://poder-judicial-test.s3.us-east-1.amazonaws.com/pdf/e057bc3b-cd4a-40c8-8fba-3f5c8dc2d1a4.pdf",
                "method": "get",
                "action": "https://oficinajudicialvirtual.pjud.cl/ADIR_871/penal/documentos/docCausaPenal.php",
                "hidden_input_name": "dtaDoc",
                "hidden_input_value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvb2ZpY2luYWp1ZGljaWFsdmlydHVhbC5wanVkLmNsIiwiYXVkIjoiaHR0cHM6XC9cL29maWNpbmFqdWRpY2lhbHZpcnR1YWwucGp1ZC5jbCIsImlhdCI6MTc1NDM2Mzc3MSwiZXhwIjoxNzU0MzY3MzcxLCJkYXRhIjoicndIaHYyVlZiZHJDdUNKd214cWZpdDE0T3IzTzdzYjZLQ09lb2ZqcUxYTXIwS3dwdlQ1Z01adkM2b3MyYVA4TGpnVXdTNEdRNzBhYkFmbGdSUkhFNHhHaEpkeHNWd2hSRER6QUtLZVRzbVZVdmQzVjdxRjNwV1FpV09WaVNaSFoifQ.b4I0kUvCb9aL8uNnjtQUvIVmbDi5mxxdvu24dJpqRLM"
            },
            {
                "s3_url": "https://poder-judicial-test.s3.us-east-1.amazonaws.com/pdf/089a90b7-f666-4a09-b7e2-0c1cf97a1216.pdf",
                "method": "get",
                "action": "https://oficinajudicialvirtual.pjud.cl/ADIR_871/penal/documentos/docCausaPenal.php",
                "hidden_input_name": "dtaDoc",
                "hidden_input_value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvb2ZpY2luYWp1ZGljaWFsdmlydHVhbC5wanVkLmNsIiwiYXVkIjoiaHR0cHM6XC9cL29maWNpbmFqdWRpY2lhbHZpcnR1YWwucGp1ZC5jbCIsImlhdCI6MTc1NDM2Mzc3MSwiZXhwIjoxNzU0MzY3MzcxLCJkYXRhIjoicndIaHYyVlZiZHJDdUNKd214cWZpcUk1Y3dQVngxeFh1T25RVUJnVVRyZzFVclNwaE9lR3hwQ0g4eWhaNVwvaTlvM3VITHF3ZE5NVEQwRmh4ZVMyZTFYVGJEUVIyb25XWDd5dTN6ZnpIZDlrPSJ9.Zh-sSpuN99QGzy3bB3jSI3aqGvSFJix4SrtrQHL9Wa8"
            }
            ],
            "extraction_datetime": "05/08/2025 03:16:12",
            "extraction_date": "05/08/2025",
            "pdfs_success_rate": 100
        }
    }
]