-include env_make

GH_VERSION ?= 1.0.0


REPO = bowens/github-pr-slack-monitor
NAME = github-pr-slack-monitor-$(GH_VERSION)

ifeq ($(TAG),)
  TAG ?= $(GH_VERSION)
endif

.PHONY: build push shell run start stop logs clean release

default: build

build:
	docker build -t $(REPO):$(TAG) ./

push:
	docker push $(REPO):$(TAG)

shell:
	docker run --rm --name $(NAME) -i -t $(PORTS) $(VOLUMES) $(ENV) $(REPO):$(TAG) /bin/bash

run:
	docker run --rm --name $(NAME) -e DEBUG=1 $(PORTS) $(VOLUMES) $(ENV) $(REPO):$(TAG) $(CMD)

start:
	docker run -d --name $(NAME) $(PORTS) $(VOLUMES) $(ENV) $(REPO):$(TAG)

stop:
	docker stop $(NAME)

logs:
	docker logs $(NAME)

clean:
	-docker rm -f $(NAME)

test:
	cd app; pytest

release: build push
