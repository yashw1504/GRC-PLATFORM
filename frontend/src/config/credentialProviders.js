export const credentialProviders = {

  aws: {
    id: "aws",
    label: "Amazon Web Services",
    icon: "☁️",
    color: "#FF9900",

    credentialTypes: [
      "IAM User",
      "Assume Role"
    ],

    fields: [
      {
        key: "name",
        label: "Credential Name",
        type: "text",
        required: true
      },
      {
        key: "accessKey",
        label: "Access Key ID",
        type: "text",
        required: true
      },
      {
        key: "secretKey",
        label: "Secret Access Key",
        type: "password",
        required: true
      },
      {
        key: "region",
        label: "Region",
        type: "select",
        options: [
          "us-east-1",
          "us-west-2",
          "eu-west-1",
          "ap-south-1",
          "ap-southeast-1"
        ]
      }
    ]
  },

  azure: {
    id: "azure",
    label: "Microsoft Azure",
    icon: "🟦",
    color: "#0078D4",

    credentialTypes: [
      "Service Principal"
    ],

    fields: [
      {
        key: "name",
        label: "Credential Name",
        type: "text",
        required: true
      },
      {
        key: "tenantId",
        label: "Tenant ID",
        type: "text"
      },
      {
        key: "subscriptionId",
        label: "Subscription ID",
        type: "text"
      },
      {
        key: "clientId",
        label: "Client ID",
        type: "text"
      },
      {
        key: "clientSecret",
        label: "Client Secret",
        type: "password"
      }
    ]
  },

  gcp: {
    id: "gcp",
    label: "Google Cloud",
    icon: "🟥",
    color: "#4285F4",

    credentialTypes: [
      "Service Account"
    ],

    fields: [
      {
        key: "name",
        label: "Credential Name",
        type: "text"
      },
      {
        key: "serviceAccount",
        label: "Service Account JSON",
        type: "file"
      }
    ]
  },

  docker: {
    id: "docker",
    label: "Docker Registry",
    icon: "🐳",
    color: "#2496ED",

    credentialTypes: [
      "Docker Hub",
      "Amazon ECR",
      "Azure ACR",
      "Google GCR",
      "Harbor"
    ],

    fields: [
      {
        key: "name",
        label: "Credential Name",
        type: "text"
      },
      {
        key: "registry",
        label: "Registry URL",
        type: "text"
      },
      {
        key: "username",
        label: "Username",
        type: "text"
      },
      {
        key: "password",
        label: "Password",
        type: "password"
      }
    ]
  },

  kubernetes: {
    id: "kubernetes",
    label: "Kubernetes",
    icon: "☸️",
    color: "#326CE5",

    credentialTypes: [
      "Kubeconfig"
    ],

    fields: [
      {
        key: "name",
        label: "Credential Name",
        type: "text"
      },
      {
        key: "kubeconfig",
        label: "Upload kubeconfig",
        type: "file"
      }
    ]
  },

  database: {
    id: "database",
    label: "Database",
    icon: "🗄️",
    color: "#10B981",

    credentialTypes: [
      "PostgreSQL",
      "MySQL",
      "SQL Server",
      "Oracle",
      "MongoDB",
      "Redis"
    ],

    fields: [
      {
        key: "name",
        label: "Credential Name",
        type: "text"
      },
      {
        key: "host",
        label: "Host",
        type: "text"
      },
      {
        key: "port",
        label: "Port",
        type: "number"
      },
      {
        key: "database",
        label: "Database Name",
        type: "text"
      },
      {
        key: "username",
        label: "Username",
        type: "text"
      },
      {
        key: "password",
        label: "Password",
        type: "password"
      }
    ]
  },

  github: {
    id: "github",
    label: "GitHub",
    icon: "🐙",
    color: "#24292F",

    credentialTypes: [
      "Personal Access Token"
    ],

    fields: [
      {
        key: "name",
        label: "Credential Name",
        type: "text"
      },
      {
        key: "token",
        label: "GitHub Token",
        type: "password"
      }
    ]
  },

  gitlab: {
    id: "gitlab",
    label: "GitLab",
    icon: "🦊",
    color: "#FC6D26",

    credentialTypes: [
      "Personal Access Token"
    ],

    fields: [
      {
        key: "name",
        label: "Credential Name",
        type: "text"
      },
      {
        key: "token",
        label: "GitLab Token",
        type: "password"
      }
    ]
  },

  api: {
    id: "api",
    label: "API Key",
    icon: "🔑",
    color: "#7C3AED",

    credentialTypes: [
      "Bearer Token",
      "API Key"
    ],

    fields: [
      {
        key: "name",
        label: "Credential Name",
        type: "text"
      },
      {
        key: "token",
        label: "Token",
        type: "password"
      }
    ]
  },

  ssh: {
    id: "ssh",
    label: "SSH",
    icon: "💻",
    color: "#64748B",

    credentialTypes: [
      "Private Key"
    ],

    fields: [
      {
        key: "name",
        label: "Credential Name",
        type: "text"
      },
      {
        key: "username",
        label: "Username",
        type: "text"
      },
      {
        key: "privateKey",
        label: "Private Key",
        type: "textarea"
      }
    ]
  }

};