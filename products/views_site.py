from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.sites.models import Site

@permission_required("sites.change_site")
def update_site_name(request):
    site = Site.objects.get_current()
    if request.method == "POST":
        new_name = request.POST.get("new_site_name")
        new_domain = request.POST.get("new_domain")
        if new_name and new_domain:
            try:
                site.name = new_name
                site.domain = new_domain
                site.save()
                messages.success(request, "Site name and domain updated successfully!")
                return redirect("admin:sites_site_change", site.id)
            except Exception as e:
                messages.error(request, f"Failed to update site: {e}")
        else:
            messages.error(request, "Both site name and domain are required.")
    # Always render the form with current site info
    return render(request, "update_site_name.html", {"site": site})
