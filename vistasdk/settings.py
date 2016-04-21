VistaService_BASE_URL = "192.168.1.210:45845"
# VistaService_BASE_URL = "127.0.0.1:8000"

VistaService_BASE_PROTOCOL = "http"

service_definitions = {

    "VistaService": {
        "resources": {
            "seats": {
                "endpoint": "/getseatlayout/",
                "required_params": [],
                "optional_params": [],
            },
            "movies": {
                "endpoint": "/getmovies/",
                "required_params": [],
                "optional_params": [],
            },
            "theatres": {
                "endpoint": "/gettheatres/",
                "required_params": [],
                "optional_params": [],
            },
            "states": {
                "endpoint": "/getshows/",
                "required_params": ["name"],
                "optional_params": [],
            },
            "screens": {
                "endpoint": "/screens/",
                "required_params": [],
                "optional_params": [],
            },
            "resource": {
                "endpoint": "/resources/",
                "required_params": [
                    "user", "start_date", "rate", "project"
                ],
                "optional_params": [
                    "end_date", "agreed_hours_per_month",
                ],
            }
        }
    }
}