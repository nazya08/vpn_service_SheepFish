"""
This file contains views and logic for managing websites within the application.
It includes functionalities for creating and managing user websites, as well as
proxying and logging access to these websites. The main classes and functions
provided are:

- `website_management_view`: Renders the main management interface where users can see and manage their websites.
- `CreateSiteView`: Handles the creation of new websites for users.
- `ProxyView`: Proxies requests to the original websites, logs traffic data, and replaces internal links with application routes.
"""
import requests

from urllib.parse import urlparse, urljoin

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View

from site_management.forms.website import WebsiteForm
from site_management.models.website import Website
from site_management.views.stats import LogAccessMixin


def website_management_view(request):
    user_websites = Website.objects.filter(user=request.user)
    return render(request, 'site_management/website_management_main.html', {'websites': user_websites})


class CreateSiteView(View):
    def get(self, request):
        form = WebsiteForm()
        return render(request, 'site_management/create_website.html', {'form': form})

    def post(self, request):
        form = WebsiteForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.user = request.user
            site.save()
            return redirect('website_management_main')
        return render(request, 'site_management/create_website.html', {'form': form})


class ProxyView(View, LogAccessMixin):
    def get(self, request, user_site_name, route=""):
        try:
            # Get the URL of the website from the database
            website = Website.objects.get(name=user_site_name)
            original_url = urljoin(website.original_url, route)

            data_uploaded = len(request.body)

            # Save the transition URL
            if request.user.is_authenticated:
                # Save the previous URL from the session or cookies
                from_url = request.session.get('previous_url', '')
                self.log_transition(request.user, website, from_url, original_url)

                # Update the URL in the session
                request.session['previous_url'] = original_url

            # Send a request to the original site
            response = requests.get(original_url)

            if response.status_code == 200:
                # Replacing all internal links with our internal routers
                content = self.replace_links(response.text, website, request)

                # Store traffic statistics
                data_downloaded = len(response.content)
                if request.user.is_authenticated:
                    self.log_access(request.user, website, data_uploaded, data_downloaded)

                return HttpResponse(content, content_type=response.headers.get('Content-Type', 'text/html'))
            else:
                return HttpResponseNotFound("The page you are looking for could not be found.")
        except Website.DoesNotExist:
            return HttpResponseNotFound("Website not found")
        except requests.RequestException as e:
            return HttpResponseNotFound(f"Error fetching the original site: {str(e)}")

    def replace_links(self, content, website, request):
        parsed_base_url = urlparse(website.original_url)
        base_url = f"{parsed_base_url.scheme}://{parsed_base_url.netloc}"

        # Replace all internal links with our internal routes
        content = content.replace(f'href="{base_url}', f'href="/{website.name}')
        content = content.replace(f'src="{base_url}', f'src="/{website.name}')

        return content
