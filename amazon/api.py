# Imports para API de Amazon
from var_config import * # Importar las variables de configuración
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
from paapi5_python_sdk.rest import ApiException

def search_items(articulo):

    """ Following are your credentials """
    """ Please add your access key here """
    access_key = ACCESS_KEY

    """ Please add your secret key here """
    secret_key = SECRET_KEY

    """ Please add your partner tag (store/tracking id) here """
    partner_tag = PARTNER_TAG

    """ PAAPI host and region to which you want to send request """
    """ For more details refer: https://webservices.amazon.com/paapi5/documentation/common-request-parameters.html#host-and-region"""
    host = "webservices.amazon.es"
    region = "eu-west-1"

    """ API declaration """
    default_api = DefaultApi(
        access_key=access_key, secret_key=secret_key, host=host, region=region
    )

    """ Request initialization"""

    # Parámetros de búsqueda
    keywords = articulo  # Palabras clave para buscar
    search_index = "All"
    item_count = 1

    # Recursos a solicitar en la API
    search_items_resource = [
        SearchItemsResource.ITEMINFO_TITLE,  # Título
        SearchItemsResource.ITEMINFO_FEATURES,  # Descripción
        SearchItemsResource.CUSTOMERREVIEWS_COUNT,  # Reseñas
        SearchItemsResource.IMAGES_PRIMARY_LARGE,  # Imagen principal
    ]

    # Crear la solicitud
    try:
        search_items_request = SearchItemsRequest(
            partner_tag=partner_tag,
            partner_type="Associates",
            keywords=keywords,
            search_index=search_index,
            item_count=item_count,
            resources=search_items_resource,
        )
    except ValueError as exception:
        print("Error al crear la solicitud:", exception)
        exit()

    # Enviar la solicitud a la API
    try:
        response = default_api.search_items(search_items_request)
        
        print("✅ API llamada con éxito")

        if response.search_result and response.search_result.items:
            item = response.search_result.items[0]  # Primer producto encontrado

            # Extraer información con validación
            title = item.item_info.title.display_value if item.item_info and item.item_info.title else "No Title"
            reviews = item.customer_reviews.count if item.customer_reviews and item.customer_reviews.count else "No Reviews"
            image_url = item.images.primary.large.url if item.images and item.images.primary else "No Image"
            description = ", ".join(item.item_info.features.display_values) if item.item_info and item.item_info.features else "No Description"
            enlace = item.detail_page_url if item.detail_page_url else "No Link"
            # Imprimir resultados
            print("\n🔹 Producto Encontrado:")
            print(f"📌 Título: {title}")
            print(f"⭐ Reseñas: {reviews}")
            print(f"🖼️ Imagen: {image_url}")
            print(f"📜 Descripción: {description}")
            print(f"🔗 Enlace: {enlace}")
            return title, reviews, image_url, description, enlace

        else:
            print("⚠️ No se encontraron productos.")
            return None, None, None, None

        # Mostrar errores si los hay
        if response.errors:
            print("\n❌ Errores:")
            for error in response.errors:
                print(f"Error {error.code}: {error.message}")
    except ApiException as e:
        print("❌ Error llamando a la API de Amazon!")
        print("Código de estado:", e.status)
        print("Detalles del error:", e.body)

    except Exception as e:
        print("❌ Error inesperado:", str(e))
        return None, None, None, None