import json
import requests
import threading
import time


def timer(func):
    def wrapper():
        start = time.perf_counter()
        func()
        finish = time.perf_counter()
        print(f'\nProgram executed in {round(finish - start, 2)} seconds.')
    return wrapper


@timer
def main():
    url_template = 'https://dummyjson.com/products/'
    file = open('products.json', 'w')
    product_list = []
    threads = []

    def get_response(num):
        nonlocal url_template
        response = requests.get(f'{url_template}{num}')
        if response.status_code == 200:
            product_list.append(response.json())
        else:
            print(response)

    for number in range(1, 101):
        thread = threading.Thread(target=get_response, args=(number,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    def sort():
        sorting = True
        current_id = 1

        while sorting:
            for product in range(0, len(product_list)):
                if current_id == product_list[product]['id']:
                    current_element = product_list[product]
                    product_list.remove(current_element)
                    product_list.append(current_element)
                    current_id += 1
                if current_id == len(product_list) + 1:
                    sorting = False

    sort()

    for product in product_list:
        if product['id'] == 1:
            file.write('[\n')
        try:
            encoded_product = json.dumps(product).encode('utf-8')
            encoded_product = encoded_product.decode('utf-8')
            file.write(f'{encoded_product}')
            if product['id'] != len(product_list):
                file.write(',\n')
        except(UnicodeError):
            print(f'Unicode error: {product}')
        if product['id'] == len(product_list):
            file.write('\n]')

    file.close()

    print(f'File filled successfully!')


if __name__ == '__main__':
    main()
