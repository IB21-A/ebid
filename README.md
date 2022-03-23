# E-bid Back End

A simulated Ebay style site that allows users to register/login. create and edit bid listings, add items to a watchlist, bid on items that aren't their own, upload images, comment on listings, and view listing stats on their profile page.

## Rebuilt from the Ground Up

This application was rebuilt from scratch from an older version. It was previously built using vanilla Django with Django's template engine for the front end with vanilla javascript and css.

The application now utilizes a Django REST Framework API that the React front end can fetch data from. The application has been deployed as one unified project. The React front-end can be seen [here](https://github.com/IB21-A/commerce-react)

### What's Different?

- Django REST API Back-end
- JWT Authentication (simplejwt)
- Django REST Serializers including
  - conditional data based on authentication and permissions
    - Does user have this listing on their watchlist?
    - Does this user have permission to access data?
  - User uploaded images (hosted on cloudinary)
  - Data validation
    - Bid amount > minumum bid
    - Listing ID exists
    - Required fields are present
- Django REST View classes including
  - Case insensitive username lookup
  - User's watchlist filtered for active listings only
  - Listing viewset with pagination optional filtering
    - Search terms
    - Category

Some troubles I faced and how I solved them:

- [Return a Boolean Value in Django REST Serializers Based on Related Models](https://dev.to/thomz/how-to-return-a-boolean-value-in-django-rest-serializers-based-on-related-models-2bm9)
- [Uploading Images to Django REST Framework from Forms in React](https://dev.to/thomz/uploading-images-to-django-rest-framework-from-forms-in-react-3jhj)
