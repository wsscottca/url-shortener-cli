# URL Shortener CLI

Welcome to the URL Shortener CLI! This command-line interface (CLI) tool interacts with the [URL Shortener API](https://github.com/wsscottca/url-shortener). It provides an easy way to shorten URLs, list all shortened URLs, look up original URLs from short URLs, and manage user authentication.

## Table of Contents

- [Installation](#installation)
- [Commands](#commands)
  - [Login](#login)
  - [Shorten URL](#shorten-url)
  - [Lookup URL](#lookup-url)
  - [List URLs](#list-urls)
- [Usage Examples](#usage-examples)

The API is deployed at [https://shrtnurl.com/](https://shrtnurl.com/) and the interactive documentation is available at [https://shrtnurl.com/docs](https://shrtnurl.com/docs).

## Installation

To install the CLI tool, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/url-shortener-cli.git
cd url-shortener-cli
pip install .
```

## Commands

### Login

**Command**: `login`

**Description**: This command allows you to log in to the API and receive a JWT token for authorization. The token is required for performing authenticated operations, such as listing URLs.

**Options**:
- `-u`, `--username` (required): The username of the account you want to log in to. It must be between 4 and 16 characters long.
- `-p`, `--password` (required): The password of the account you want to log in to. It must be between 8 and 32 characters long.

**Usage**:
```bash
url-shortener login -u yourusername -p yourpassword
```

### Shorten URL

**Command**: `shorten`

**Description**: This command shortens a given valid URL. You can optionally provide your own short URL code if you want to specify a custom alias. If no short URL code is provided, the system will generate a unique code.

**Options**:
- `--url` (required): The URL that you want to shorten. It must be a valid web address.
- `--short-url`: An optional custom short URL string. If provided, it must be no longer than 8 characters.

**Usage**:
```bash
url-shortener shorten --url http://example.com --short-url shorty
```

### Lookup URL

**Command**: `lookup`

**Description**: This command retrieves the original URL associated with a given short URL. This is useful if you have a short URL and want to find out what original URL it redirects to.

**Options**:
- `--short-url` (required): The short URL that you want to look up. It must be a valid short URL code.

**Usage**:
```bash
url-shortener lookup --short-url shorty
```

### List URLs

**Command**: `list_urls`

**Description**: This command lists all URL pairs (short URL and original URL) stored in the system. This command requires admin privileges, so you need to be logged in as an administrator to use it.

**Options**:
- `--admin` (flag): This flag indicates that the command should be run with administrator privileges. You must be logged in and have a valid admin token to use this command.

**Usage**:
```bash
url-shortener list_urls --admin
```

## Usage Examples

### Login

```bash
url-shortener login -u yourusername -p yourpassword
```

- **Description**: This command logs you in to the API using your username and password. If successful, it retrieves a JWT token for subsequent authorized requests.

**Response:**
```
Successfully retrieved token.
```

### Shorten a URL

```bash
url-shortener shorten --url http://example.com --short-url shorty
```

- **Description**: This command shortens the given URL (`http://example.com`) and associates it with the provided short URL code (`shorty`). If no short URL code is provided, a unique code will be generated.

**Response:**
```bash
Successfully created short URL.
Short URL: https://shrtnurl.com/shorty
URL: http://example.com
```

### Lookup URL

```bash
url-shortener lookup --short-url shorty
```

- **Description**: This command looks up the original URL associated with the provided short URL (`shorty`).

**Response:**
```
http://example.com
```

### List URLs

To list all URL pairs in the system, you need to be logged in as an administrator. Use the following credentials for testing: 
- Username: `test`
- Password: `password`

First, log in with admin credentials:

```bash
url-shortener login -u test -p password
```

Then, list all URLs:

```bash
url-shortener list_urls --admin
```

- **Description**: This command lists all URL pairs in the system. It requires the user to be logged in with admin privileges.

**Response:**
```
ShortUrl -> Url
shorty1 -> http://example1.com
shorty2 -> http://example2.com
```

This README provides a comprehensive guide for using the URL Shortener CLI to interact with the [URL Shortener API](https://github.com/wsscottca/url-shortener) effectively.