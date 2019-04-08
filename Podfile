
platform :ios, '11.4'
swift_version = '5.0'

target '***' do
  # Comment the next line if you're not using Swift and don't want to use dynamic frameworks
  use_frameworks!

  # Funtasty architecture pods
  pod 'FuntastyKit', git: 'https://github.com/thefuntasty/FuntastyKit.git', tag: 'v1.2.3'
  pod 'FTAPIKit', git: 'https://github.com/thefuntasty/FTAPIKit.git', tag: 'v0.3.1'
  pod 'FTAPIKit', git: 'https://github.com/thefuntasty/FTAPIKit.git', subspecs: ['PromiseKit'], tag: 'v0.3.1'
  pod 'CellKit', git: 'https://github.com/thefuntasty/CellKit.git', tag: 'v0.2'

  # Third-party pods
  pod 'PromiseKit', '~> 6.0'

  # Tools
  pod 'SwiftLint'

  target '***Tests' do
    inherit! :search_paths
    # Pods for testing
  end
end
