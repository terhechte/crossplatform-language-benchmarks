import Foundation

struct User: Codable {
    let username: String
}

struct Comment: Codable {
    let author: User
    let text: String
    let likes: [User]
}

struct Media: Codable {
    let author: User
    let likes: [User]
    let comments: [Comment]
    let images: [String: String]
    let description: String
}

func process(input: Data) {
    let parsed = try! JSONDecoder().decode([Media].self, from: input)
    print(parsed.map { $0.author.username })
}

func main() {
    let data = try! Data(contentsOf: URL(fileURLWithPath: "./test.json"))
    process(input: data)
}
main()
