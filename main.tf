terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.12.0"
    }
  }
}

provider "google" {
  project     = "unified-era-355307"
  region      = "us-central1"
  credentials = "/home/german/globant/sa-ubuntuzenbook.json"
}

resource "google_cloud_run_service" "example" {
  name     = "database-app"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/unified-era-355307/databaseapp:public"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}



#resource "google_compute_instance" "my_instance" {
#    name = "terraform-instance"
#    machine_type = "e2-micro"
#    zone = "us-central1-a"

#    boot_disk {
#      initialize_params {
#        image = "ubuntu-2004-focal-v20240110"
#      }
#    }

#    network_interface {
#      network = "default"
#      access_config {
        
#      }
      
#    }
#metadata_startup_script = "sudo docker run -p 8501:8501 database_migration_app"
#}