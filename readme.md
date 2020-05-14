docker exec -it 3e8747788b99 bash
docker exec -it 3e8747788b99 python train_model.py

curl --header "Content-Type: application/json" --request POST --data '{"flower":"1,2,3,7"}' http://192.168.99.100:5000/iris_post


curl -H "Content-Type: application/json" -X POST http://192.168.99.100:5000/iris_post -d @test.json