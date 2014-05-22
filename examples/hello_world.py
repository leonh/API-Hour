import os
import asyncio
import aiohttp
import aiorest


def handler():
    return {'hello': 'world'}


def say_hello(name: str):
    return 'Hello, {}!'.format(name)


def main():
    loop = asyncio.get_event_loop()

    server = aiorest.RESTServer(hostname='127.0.0.1', loop=loop)
    server.add_url('GET', '/hello-world', handler)
    server.add_url('GET', '/hello/{name}', say_hello)

    srv = loop.run_until_complete(loop.create_server(
        server.make_handler, '127.0.0.1', 8080))

    @asyncio.coroutine
    def query():
        resp = yield from aiohttp.request(
            'GET', 'http://127.0.0.1:8080/hello-world',
            loop=loop)
        json_data = yield from resp.read_and_close(decode=True)
        print(json_data)

        name = os.environ.get('USER', 'John')
        resp = yield from aiohttp.request(
            'GET', 'http://127.0.0.1:8080/hello/{}'.format(name))
        json_data = yield from resp.read_and_close(decode=True)
        print(json_data)

    loop.run_until_complete(query())
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.close()


if __name__ == '__main__':
    main()
