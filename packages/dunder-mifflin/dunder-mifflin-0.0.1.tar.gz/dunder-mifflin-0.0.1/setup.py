# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 3 - Alpha"

setuptools.setup(
    name="dunder-mifflin",
    version="0.0.1",
    description="Out of paper, out of stock. These friendly faces around the "
    + "block. Break loose from the chains that are causing you "
    + "pain. Call Michael, Stanley, Jim, Dwight, or Creed Call Andy "
    + "and Kelly for your business paper needs.",
    url="",
    author="",
    author_email="",
    license="Apache 2.0",
    classifiers=[
        release_status,
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    zip_safe=False,
)
