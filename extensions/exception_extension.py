from werkzeug.exceptions import HTTPException

def register_exception_handler(app: Flask):
    @app.errorhandler(Exception)
    def handle_global_error(error: HTTPException):
        """ Make JSON Error Response instead of Web Page """
        response = {
            'error': error.__class__.__name__,
            'message': error.description,
        }
        return response, error.code
